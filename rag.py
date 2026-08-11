"""
================================================================================
rag.py — Retrieval-Augmented Generation layer for the DSA Coach Agent
================================================================================

PURPOSE
-------
This module is the RETRIEVAL layer of the DSA Coach Agent. Given a student's
question (plus optional filters like topic/difficulty/user_id), it:

    1. Understands the student's intent (LEARN, STORY, PRACTICE, HINT, ...)
    2. Embeds the query using a sentence embedding model
    3. Retrieves candidate chunks from PostgreSQL + pgvector
    4. Filters, reranks, deduplicates, and balances those candidates
    5. Builds a clean, structured text context

It does **NOT** call an LLM and does **NOT** generate the coach's final
answer. That responsibility belongs to `coach.py`. This file only answers
the question: "What information is relevant to show the LLM?"

ARCHITECTURE
------------
    Streamlit UI (Learn / Practice / Code Review)
                |
                v
        rag.retrieve_context(...)   <-- THIS FILE
                |
                v
        {context, documents, intent, sources, retrieval_stats}
                |
                v
              coach.py  ---->  LLM  ---->  DSA Coach answer

EXPECTED DATABASE TABLE
------------------------
    CREATE TABLE rag_chunks (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        metadata JSONB,
        embedding VECTOR(384)
    );

Metadata (JSONB) is expected to contain keys such as:
    content_type   -> "dsa" | "story" | "description" | "leetcode" | "student_code"
    topic           -> e.g. "Array", "Stack", "Binary Search"
    difficulty      -> "Easy" | "Medium" | "Hard"   (leetcode only)
    title           -> problem title                (leetcode only)
    question_id     -> problem id                    (leetcode only)
    file_type       -> "py" | "ipynb"                (student_code only)
    user_id         -> owner of the code              (student_code only)
    filename        -> original filename              (student_code only)
    source          -> human-readable source name

EMBEDDING MODEL
----------------
    BAAI/bge-small-en-v1.5  (384-dimensional embeddings)

    BGE models recommend prefixing *queries* (not stored documents) with an
    instruction string to improve retrieval quality. This module applies
    that prefix automatically when embedding a student's question.

RETRIEVAL FLOW
---------------
    question
       -> input validation
       -> intent detection (rule-based, no extra LLM call)
       -> query embedding
       -> per-category candidate retrieval (dsa/story/description/leetcode/code)
       -> similarity threshold filtering
       -> deduplication
       -> lightweight reranking (similarity + topic/difficulty/intent match)
       -> category-balanced selection (respecting max_context_chunks)
       -> context formatting (respecting max_context_characters)
       -> structured result returned to coach.py

PUBLIC API
----------
    retrieve_context(
        question,
        mode="general",         # general | learn | story | practice | hint |
                                 # solution | code_review | debug
        topic=None,
        difficulty=None,
        user_id=None,
        include_code=False,
        k=None,                 # backward-compat: overrides max_context_chunks
        include_leetcode=True,  # backward-compat flag
        include_stories=True,   # backward-compat flag
    ) -> {
        "context": str,
        "documents": list[dict],
        "intent": str,
        "sources": list[dict],
        "retrieval_stats": dict,
    }

    This module-level function is a thin wrapper around a lazily-created,
    module-level `DSA_RAG` instance, so `coach.py` can simply do:

        from rag import retrieve_context
        result = retrieve_context("What is a stack?", mode="learn")

    For finer control (custom DB config, custom thresholds, etc.), construct
    your own `DSA_RAG(...)` instance directly.

SECURITY NOTES
---------------
    * Database credentials are read from environment variables (.env via
      python-dotenv) and are NEVER logged or printed.
    * All SQL is parameterized. No user input is ever concatenated into a
      SQL string.
    * Student code retrieval always requires an explicit `user_id` and is
      always filtered by it — one student's code is never returned for
      another student's query.
================================================================================
"""

from __future__ import annotations

import os
import re
import json
import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence
from config import EMBEDDING_MODEL,EMBEDDING_DIMENSION,TOP_K
from database import get_connection
from langchain_huggingface import HuggingFaceEmbeddings

# --------------------------------------------------------------------------
# Optional dependencies are imported defensively so that import errors turn
# into clear runtime errors (with safe fallbacks) rather than crashing the
# whole application at import time.
# --------------------------------------------------------------------------
try:
    import psycopg2
    import psycopg2.extras
except ImportError:  # pragma: no cover - environment dependent
    psycopg2 = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - environment dependent
    SentenceTransformer = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is optional
    pass


# --------------------------------------------------------------------------
# Logging — never log secrets (passwords, full DB URLs, etc.)
# --------------------------------------------------------------------------
logger = logging.getLogger("dsa_coach.rag")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(_handler)
logger.setLevel(os.environ.get("RAG_LOG_LEVEL", "INFO"))


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
EMBEDDING_MODEL_NAME = EMBEDDING_MODEL
EMBEDDING_DIM = EMBEDDING_DIMENSION

# BGE-family models recommend prefixing queries (not documents) with this
# instruction to improve retrieval relevance.
BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

VALID_CONTENT_TYPES = {"dsa", "story", "description", "leetcode", "student_code"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
VALID_MODES = {
    "general", "learn", "story", "practice", "hint",
    "solution", "code_review", "debug",
}

INTENTS = {
    "LEARN", "EXPLAIN", "STORY", "HINT", "PRACTICE", "SOLUTION",
    "CODE_REVIEW", "DEBUG", "COMPLEXITY", "LEETCODE", "GENERAL",
}

# Mode -> canonical intent (used when the caller explicitly picks a mode
# instead of relying on automatic intent detection).
MODE_TO_INTENT = {
    "general": None,  # fall back to detect_intent()
    "learn": "LEARN",
    "story": "STORY",
    "practice": "PRACTICE",
    "hint": "HINT",
    "solution": "SOLUTION",
    "code_review": "CODE_REVIEW",
    "debug": "DEBUG",
}


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
@dataclass
class RAGConfig:
    """All tunable knobs for retrieval live here so behavior can be changed
    without touching retrieval logic."""

    # --- database connection (read from environment; never hard-coded) ---
    db_host: str = field(default_factory=lambda: os.environ.get("DB_HOST", "localhost"))
    db_port: str = field(default_factory=lambda: os.environ.get("DB_PORT", "5432"))
    db_name: str = field(default_factory=lambda: os.environ.get("DB_NAME", "dsa_coach"))
    db_user: str = field(default_factory=lambda: os.environ.get("DB_USER", "postgres"))
    db_password: str = field(default_factory=lambda: os.environ.get("DB_PASSWORD", ""))

    # --- embedding ---
    embedding_model_name: str = EMBEDDING_MODEL_NAME

    # --- retrieval sizing ---
    candidate_k: int = 18            # candidates retrieved per category before filtering
    max_context_chunks: int = 8      # final chunks sent to coach.py
    max_context_characters: int = 12000

    # --- quality gates ---
    similarity_threshold: float = 0.60

    # --- reranking weights (must roughly sum to something sane; tune freely) ---
    weight_similarity: float = 0.55
    weight_topic_match: float = 0.20
    weight_difficulty_match: float = 0.10
    weight_content_type_relevance: float = 0.10
    weight_intent_match: float = 0.05


# --------------------------------------------------------------------------
# Category weighting per intent, used for balanced (non-dominated) selection.
# Higher weight = more "slots" reserved for that content_type when the pool
# allows it. "student_code" covers both py and ipynb sub-types together.
# --------------------------------------------------------------------------
INTENT_CATEGORY_PLAN: Dict[str, Dict[str, int]] = {
    "LEARN":       {"dsa": 2, "description": 1, "story": 1},
    "EXPLAIN":     {"dsa": 2, "description": 1},
    "STORY":       {"story": 2, "description": 1, "dsa": 1},
    "HINT":        {"dsa": 1, "leetcode": 1, "description": 1},
    "PRACTICE":    {"leetcode": 5, "dsa": 1},
    "LEETCODE":    {"leetcode": 5, "dsa": 1},
    "SOLUTION":    {"dsa": 2, "leetcode": 1, "description": 1},
    "CODE_REVIEW": {"student_code": 3, "dsa": 2, "description": 1},
    "DEBUG":       {"student_code": 3, "dsa": 2, "description": 1},
    "COMPLEXITY":  {"dsa": 2, "description": 2},
    "GENERAL":     {"dsa": 1, "description": 1, "story": 1, "leetcode": 1},
}

# Which content_types are worth querying at all for a given intent (used to
# avoid unnecessary DB round-trips, e.g. don't hit the leetcode table for a
# pure STORY question).
INTENT_ACTIVE_CATEGORIES: Dict[str, set] = {
    "LEARN": {"dsa", "description", "story"},
    "EXPLAIN": {"dsa", "description"},
    "STORY": {"story", "description", "dsa"},
    "HINT": {"dsa", "leetcode", "description"},
    "PRACTICE": {"leetcode", "dsa"},
    "LEETCODE": {"leetcode", "dsa"},
    "SOLUTION": {"dsa", "leetcode", "description"},
    "CODE_REVIEW": {"student_code", "dsa", "description"},
    "DEBUG": {"student_code", "dsa", "description"},
    "COMPLEXITY": {"dsa", "description"},
    "GENERAL": {"dsa", "description", "story", "leetcode"},
}


# --------------------------------------------------------------------------
# Exceptions — kept simple and specific so callers (coach.py) can decide
# how to react without the whole app crashing.
# --------------------------------------------------------------------------
class RAGError(Exception):
    """Base class for all recoverable RAG errors."""


class RAGConnectionError(RAGError):
    """Raised when the database is unreachable."""


class RAGEmbeddingError(RAGError):
    """Raised when the embedding model fails to embed the query."""


# ==========================================================================
# Main class
# ==========================================================================
class DSA_RAG:
    """Encapsulates all retrieval logic for the DSA Coach Agent.

    Instantiate once (it lazily loads the embedding model) and reuse across
    requests — creating a new instance per query would reload the model
    every time, which is slow.
    """

    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self._embedding_model = None  # lazy-loaded

    # ----------------------------------------------------------------
    # Embedding model
    # ----------------------------------------------------------------
    def _load_embedding_model(self):
        if self._embedding_model is not None:
            return self._embedding_model

        if SentenceTransformer is None:
            raise RAGEmbeddingError(
                "sentence-transformers is not installed. "
                "Install it with: pip install sentence-transformers"
            )

        try:
            logger.info("Loading embedding model: %s", self.config.embedding_model_name)
            self._embedding_model = SentenceTransformer(self.config.embedding_model_name)
        except Exception as exc:
            raise RAGEmbeddingError(f"Failed to load embedding model: {exc}") from exc

        return self._embedding_model

    def create_query_embedding(self, text: str) -> List[float]:
        """Convert a student's query string into a 384-dim embedding vector.

        Applies the BGE query instruction prefix, which measurably improves
        retrieval quality for bge-* models (documents were indexed WITHOUT
        this prefix at ingestion time, which is the correct asymmetric
        setup for BGE).
        """
        if not text or not text.strip():
            raise RAGEmbeddingError("Cannot embed an empty query.")

        model = self._load_embedding_model()
        try:
            prefixed = f"{BGE_QUERY_INSTRUCTION}{text.strip()}"
            vector = model.encode(prefixed, normalize_embeddings=True)
            return [float(x) for x in vector]
        except Exception as exc:
            raise RAGEmbeddingError(f"Failed to embed query: {exc}") from exc

    # ----------------------------------------------------------------
    # Database connection
    # ----------------------------------------------------------------
    def get_connection(self):
        """Open a new PostgreSQL connection using environment-provided
        credentials. Never logs the password."""
        if psycopg2 is None:
            raise RAGConnectionError(
                "psycopg2 is not installed. Install it with: pip install psycopg2-binary"
            )

        cfg = self.config
        try:
            conn = psycopg2.connect(
                host=cfg.db_host,
                port=cfg.db_port,
                dbname=cfg.db_name,
                user=cfg.db_user,
                password=cfg.db_password,
            )
            return conn
        except Exception as exc:
            # Deliberately avoid including cfg.db_password in the log/error.
            logger.error(
                "Database connection failed (host=%s, db=%s, user=%s): %s",
                cfg.db_host, cfg.db_name, cfg.db_user, type(exc).__name__,
            )
            raise RAGConnectionError("Could not connect to the database.") from exc

    # ----------------------------------------------------------------
    # Intent detection (rule-based; no extra LLM call)
    # ----------------------------------------------------------------
    @staticmethod
    def detect_intent(question: str) -> str:
        """Lightweight keyword/regex based intent classifier.

        Order matters: more specific intents are checked before more
        general ones so e.g. "why is my code giving TLE" is classified as
        DEBUG rather than the more generic EXPLAIN.
        """
        q = (question or "").lower().strip()
        if not q:
            return "GENERAL"

        rules: List[tuple] = [
            ("DEBUG", [
                r"\btle\b", r"time limit exceeded", r"wrong answer", r"\bbug\b",
                r"\berror\b", r"not working", r"\bdebug\b", r"\bfails?\b",
                r"runtime error", r"segmentation fault", r"exception",
                r"stack trace", r"traceback",
            ]),
            ("CODE_REVIEW", [
                r"review my code", r"review this code", r"code review",
                r"feedback on my code", r"check my code", r"improve my code",
                r"critique my (code|solution)",
            ]),
            ("COMPLEXITY", [
                r"time complexity", r"space complexity", r"big[\s-]?o",
                r"complexity of", r"how efficient",
            ]),
            ("SOLUTION", [
                r"\bsolution\b", r"solve this", r"full solution",
                r"complete solution", r"answer to this problem",
                r"give me the answer",
            ]),
            ("HINT", [
                r"\bhint\b", r"i'?m stuck", r"nudge me", r"small clue",
                r"point me in the right direction",
            ]),
            ("LEETCODE", [
                r"leetcode", r"practice problem", r"give me a problem",
                r"easy problem", r"medium problem", r"hard problem",
                r"coding problem", r"practice question", r"another problem",
            ]),
            ("STORY", [
                r"\bstory\b", r"analogy", r"real[\s-]?world", r"like i'?m 5",
                r"\beli5\b", r"simple explanation", r"beginner explanation",
                r"explain .* using",
            ]),
            ("EXPLAIN", [
                r"^explain\b", r"how does", r"how do", r"^why\b", r"walk me through",
            ]),
            ("LEARN", [
                r"^what is\b", r"^what's\b", r"\bdefine\b", r"definition of",
                r"learn about", r"introduce", r"tell me about",
            ]),
        ]

        for intent, patterns in rules:
            for pattern in patterns:
                if re.search(pattern, q):
                    return intent

        return "GENERAL"

    # ----------------------------------------------------------------
    # Core semantic search against pgvector
    # ----------------------------------------------------------------
    def semantic_search(
        self,
        query_embedding: Sequence[float],
        content_type: Optional[str] = None,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        user_id: Optional[str] = None,
        file_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Run a parameterized cosine-similarity search against rag_chunks,
        with optional metadata filters applied in SQL (so irrelevant rows
        are never pulled across the wire in the first place).

        Returns a list of dicts: {id, content, metadata, similarity}.
        Never raises on "no results" — returns an empty list instead.
        """
        limit = limit or self.config.candidate_k

        # pgvector expects a literal like '[0.1,0.2,...]' cast to ::vector
        vector_literal = "[" + ",".join(repr(float(x)) for x in query_embedding) + "]"

        where_clauses = ["embedding IS NOT NULL"]
        params: List[Any] = []

        if content_type:
            where_clauses.append("metadata->>'content_type' = %s")
            params.append(content_type)
        if topic:
            where_clauses.append("LOWER(metadata->>'topic') = LOWER(%s)")
            params.append(topic)
        if difficulty:
            where_clauses.append("LOWER(metadata->>'difficulty') = LOWER(%s)")
            params.append(difficulty)
        if file_type:
            where_clauses.append("metadata->>'file_type' = %s")
            params.append(file_type)
        if user_id is not None:
            where_clauses.append("metadata->>'user_id' = %s")
            params.append(str(user_id))

        where_sql = " AND ".join(where_clauses)

        # <=> is pgvector's cosine-distance operator (0 = identical). We
        # convert to a similarity score (higher = better) for downstream
        # thresholding/reranking, which is more intuitive to work with.
        sql = f"""
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> %s::vector) AS similarity
            FROM rag_chunks
            WHERE {where_sql}
            ORDER BY embedding <=> %s::vector ASC
            LIMIT %s
        """
        # vector literal is used twice (SELECT + ORDER BY) plus once per
        # filter above, then LIMIT.
        query_params = [vector_literal] + params + [vector_literal, limit]

        try:
            conn = self.get_connection()
        except RAGConnectionError:
            logger.error("semantic_search aborted: no database connection.")
            return []

        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(sql, query_params)
                    rows = cur.fetchall()
        except Exception as exc:
            logger.error("semantic_search query failed: %s", type(exc).__name__)
            return []
        finally:
            try:
                conn.close()
            except Exception:
                pass

        results: List[Dict[str, Any]] = []
        for row in rows:
            metadata = row.get("metadata") or {}
            if isinstance(metadata, str):
                # Defensive: some drivers may return JSONB as a raw string.
                try:
                    metadata = json.loads(metadata)
                except (json.JSONDecodeError, TypeError):
                    metadata = {}
            results.append({
                "id": row.get("id"),
                "content": row.get("content") or "",
                "metadata": metadata,
                "similarity": float(row.get("similarity") or 0.0),
            })
        return results

    # ----------------------------------------------------------------
    # Per-category retrieval helpers
    # ----------------------------------------------------------------
    def retrieve_dsa_knowledge(self, query_embedding, topic=None, limit=None):
        return self.semantic_search(
            query_embedding, content_type="dsa", topic=topic, limit=limit,
        )

    def retrieve_stories(self, query_embedding, topic=None, limit=None):
        return self.semantic_search(
            query_embedding, content_type="story", topic=topic, limit=limit,
        )

    def retrieve_descriptions(self, query_embedding, topic=None, limit=None):
        return self.semantic_search(
            query_embedding, content_type="description", topic=topic, limit=limit,
        )

    def retrieve_leetcode(self, query_embedding, topic=None, difficulty=None, limit=None):
        return self.semantic_search(
            query_embedding, content_type="leetcode",
            topic=topic, difficulty=difficulty, limit=limit,
        )

    def retrieve_python_code(self, query_embedding, user_id, topic=None, limit=None):
        """Student .py retrieval. `user_id` is REQUIRED — one student's
        code must never leak into another student's context."""
        if not user_id:
            logger.warning("retrieve_python_code called without user_id — skipping.")
            return []
        return self.semantic_search(
            query_embedding, content_type="student_code", file_type="py",
            user_id=user_id, topic=topic, limit=limit,
        )

    def retrieve_notebook_code(self, query_embedding, user_id, topic=None, limit=None):
        """Student .ipynb retrieval. `user_id` is REQUIRED for the same
        privacy reason as retrieve_python_code."""
        if not user_id:
            logger.warning("retrieve_notebook_code called without user_id — skipping.")
            return []
        return self.semantic_search(
            query_embedding, content_type="student_code", file_type="ipynb",
            user_id=user_id, topic=topic, limit=limit,
        )

    # ----------------------------------------------------------------
    # Similarity threshold
    # ----------------------------------------------------------------
    def apply_similarity_threshold(
        self, documents: List[Dict[str, Any]], threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        threshold = self.config.similarity_threshold if threshold is None else threshold
        return [d for d in documents if d.get("similarity", 0.0) >= threshold]

    # ----------------------------------------------------------------
    # Deduplication
    # ----------------------------------------------------------------
    @staticmethod
    def deduplicate_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates by stable chunk id first, then by a content
        hash (catches the same text being retrieved under two different
        content_type searches, e.g. an overlapping dsa+description chunk)."""
        seen_ids = set()
        seen_hashes = set()
        deduped: List[Dict[str, Any]] = []

        for doc in documents:
            doc_id = doc.get("id")
            if doc_id is not None:
                if doc_id in seen_ids:
                    continue
                seen_ids.add(doc_id)

            content_hash = hashlib.md5(
                (doc.get("content") or "").strip().encode("utf-8")
            ).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            deduped.append(doc)

        return deduped

    # ----------------------------------------------------------------
    # Reranking
    # ----------------------------------------------------------------
    def rerank_documents(
        self,
        documents: List[Dict[str, Any]],
        intent: str,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Lightweight (non-cross-encoder) reranker. Combines:
            - raw semantic similarity
            - topic match bonus
            - difficulty match bonus
            - content-type relevance for the current intent
            - flat intent-match bonus (content_type is "active" for intent)
        into a single score, then sorts descending.
        """
        cfg = self.config
        active_categories = INTENT_ACTIVE_CATEGORIES.get(intent, set())
        category_plan = INTENT_CATEGORY_PLAN.get(intent, {})
        max_plan_weight = max(category_plan.values()) if category_plan else 1

        scored: List[Dict[str, Any]] = []
        for doc in documents:
            meta = doc.get("metadata", {}) or {}
            similarity = doc.get("similarity", 0.0)

            topic_match = 0.0
            if topic and str(meta.get("topic", "")).lower() == str(topic).lower():
                topic_match = 1.0

            difficulty_match = 0.0
            if difficulty and str(meta.get("difficulty", "")).lower() == str(difficulty).lower():
                difficulty_match = 1.0

            content_type = meta.get("content_type", "")
            content_type_relevance = (
                category_plan.get(content_type, 0) / max_plan_weight
                if category_plan else 0.0
            )

            intent_match = 1.0 if content_type in active_categories else 0.0

            score = (
                cfg.weight_similarity * similarity
                + cfg.weight_topic_match * topic_match
                + cfg.weight_difficulty_match * difficulty_match
                + cfg.weight_content_type_relevance * content_type_relevance
                + cfg.weight_intent_match * intent_match
            )

            doc_with_score = dict(doc)
            doc_with_score["rerank_score"] = score
            scored.append(doc_with_score)

        scored.sort(key=lambda d: d["rerank_score"], reverse=True)
        return scored

    # ----------------------------------------------------------------
    # Balanced category selection
    # ----------------------------------------------------------------
    def select_balanced_context(
        self,
        documents: List[Dict[str, Any]],
        intent: str,
        max_chunks: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Prevents one content_type from dominating the final context.

        Documents must already be sorted best-first (post-rerank). We walk
        the category plan, taking up to N documents per category, then fill
        any remaining slots (up to max_context_chunks) with whatever is
        left, best score first.
        """
        max_chunks = (
            max_chunks
            if max_chunks is not None
            else self.config.max_context_chunks
        )
        plan = INTENT_CATEGORY_PLAN.get(intent, {})

        by_category: Dict[str, List[Dict[str, Any]]] = {}
        for doc in documents:
            content_type = (doc.get("metadata", {}) or {}).get("content_type", "unknown")
            by_category.setdefault(content_type, []).append(doc)

        selected: List[Dict[str, Any]] = []
        selected_ids = set()

        # Pass 1: honor the per-category plan quotas.
        for content_type, quota in plan.items():
            for doc in by_category.get(content_type, [])[:quota]:
                if len(selected) >= max_chunks:
                    break
                key = doc.get("id") if doc.get("id") is not None else id(doc)
                if key in selected_ids:
                    continue
                selected.append(doc)
                selected_ids.add(key)

        # Pass 2: fill any remaining slots with the next-best documents
        # overall, regardless of category, without exceeding max_chunks.
        if len(selected) < max_chunks:
            for doc in documents:
                if len(selected) >= max_chunks:
                    break
                key = doc.get("id") if doc.get("id") is not None else id(doc)
                if key in selected_ids:
                    continue
                selected.append(doc)
                selected_ids.add(key)

        return selected[:max_chunks]

    # ----------------------------------------------------------------
    # Context formatting
    # ----------------------------------------------------------------
    def format_documents(self, documents: List[Dict[str, Any]]) -> str:
        """Builds a clearly-sectioned text context, grouped by content_type,
        stopping once max_context_characters is reached."""
        max_chars = self.config.max_context_characters

        section_titles = {
            "dsa": "DSA KNOWLEDGE",
            "description": "DESCRIPTION",
            "story": "STORY",
            "leetcode": "LEETCODE",
            "student_code": "STUDENT CODE",
        }

        # Group while preserving relative (already-ranked) order.
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for doc in documents:
            content_type = (doc.get("metadata", {}) or {}).get("content_type", "unknown")
            grouped.setdefault(content_type, []).append(doc)

        pieces: List[str] = []
        total_len = 0
        truncated = False

        for content_type, docs in grouped.items():
            title = section_titles.get(content_type, content_type.upper())
            for doc in docs:
                meta = doc.get("metadata", {}) or {}
                header_lines = [f"===== {title} ====="]

                if content_type == "leetcode":
                    if meta.get("title"):
                        header_lines.append(f"Title: {meta['title']}")
                    if meta.get("difficulty"):
                        header_lines.append(f"Difficulty: {meta['difficulty']}")
                    if meta.get("topic"):
                        header_lines.append(f"Topic: {meta['topic']}")
                elif content_type == "student_code":
                    if meta.get("filename"):
                        header_lines.append(f"Filename: {meta['filename']}")
                    if meta.get("file_type"):
                        header_lines.append(f"File Type: {meta['file_type']}")
                    if meta.get("topic"):
                        header_lines.append(f"Topic: {meta['topic']}")
                else:
                    if meta.get("source"):
                        header_lines.append(f"Source: {meta['source']}")
                    if meta.get("topic"):
                        header_lines.append(f"Topic: {meta['topic']}")

                block = "\n".join(header_lines) + "\n\n" + (doc.get("content") or "").strip() + "\n"

                if total_len + len(block) > max_chars:
                    truncated = True
                    break
                pieces.append(block)
                total_len += len(block)
            if truncated:
                break

        context = "\n".join(pieces).strip()
        if truncated:
            context += "\n\n[context truncated at max_context_characters]"
        return context

    # ----------------------------------------------------------------
    # Retrieval plan construction
    # ----------------------------------------------------------------
    def _build_active_categories(
        self,
        intent: str,
        include_code: bool,
        include_leetcode: bool,
        include_stories: bool,
        user_id: Optional[str],
    ) -> set:
        """Applies backward-compat flags on top of the intent's default
        active-category set."""
        categories = set(INTENT_ACTIVE_CATEGORIES.get(intent, {"dsa", "description"}))

        if not include_leetcode:
            categories.discard("leetcode")
        if not include_stories:
            categories.discard("story")

        wants_code = include_code or intent in ("CODE_REVIEW", "DEBUG")
        if wants_code and user_id:
            categories.add("student_code")
        else:
            categories.discard("student_code")

        return categories

    # ----------------------------------------------------------------
    # Public orchestration method
    # ----------------------------------------------------------------
    def retrieve_context(
        self,
        question: str,
        mode: str = "general",
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        user_id: Optional[str] = None,
        include_code: bool = False,
        k: Optional[int] = None,
        include_leetcode: bool = True,
        include_stories: bool = True,
    ) -> Dict[str, Any]:
        """Main entry point. See module docstring for the return shape."""

        stats: Dict[str, Any] = {
            "candidates_retrieved": {},
            "after_similarity_threshold": 0,
            "after_dedup": 0,
            "final_chunk_count": 0,
            "errors": [],
        }

        # ---- 1. Input validation --------------------------------------
        if not question or not question.strip():
            logger.warning("retrieve_context called with an empty question.")
            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {**stats, "errors": ["empty_query"]},
            }

        mode = (mode or "").strip().lower()

        if mode not in VALID_MODES:
            logger.warning("Unknown mode '%s' — falling back to 'general'.", mode)
            mode = "general"

        if difficulty and difficulty.lower() not in VALID_DIFFICULTIES:
            logger.warning("Unknown difficulty '%s' — ignoring filter.", difficulty)
            difficulty = None

        # backward-compat: `k` overrides max_context_chunks for this call only.
        # IMPORTANT: do not mutate self.config because the default RAG instance
        # is shared across Streamlit requests.
        effective_max_chunks = (
            int(k) if k is not None and int(k) > 0
            else self.config.max_context_chunks
        )

        try:
            # ---- 2. Intent detection -----------------------------------
            mapped_intent = MODE_TO_INTENT.get(mode)
            intent = mapped_intent or self.detect_intent(question)

            # ---- 3. Query embedding -------------------------------------
            try:
                query_embedding = self.create_query_embedding(question)
            except RAGEmbeddingError as exc:
                logger.error("Embedding failed: %s", exc)
                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": {**stats, "errors": ["embedding_failed"]},
                }

            # ---- 4. Determine which categories to query -----------------
            active_categories = self._build_active_categories(
                intent, include_code, include_leetcode, include_stories, user_id,
            )

            # ---- 5. Candidate retrieval per category ---------------------
            candidates: List[Dict[str, Any]] = []

            if "dsa" in active_categories:
                docs = self.retrieve_dsa_knowledge(query_embedding, topic=topic)
                stats["candidates_retrieved"]["dsa"] = len(docs)
                candidates.extend(docs)

            if "description" in active_categories:
                docs = self.retrieve_descriptions(query_embedding, topic=topic)
                stats["candidates_retrieved"]["description"] = len(docs)
                candidates.extend(docs)

            if "story" in active_categories:
                docs = self.retrieve_stories(query_embedding, topic=topic)
                stats["candidates_retrieved"]["story"] = len(docs)
                candidates.extend(docs)

            if "leetcode" in active_categories:
                docs = self.retrieve_leetcode(query_embedding, topic=topic, difficulty=difficulty)
                stats["candidates_retrieved"]["leetcode"] = len(docs)
                candidates.extend(docs)

            if "student_code" in active_categories and user_id:
                py_docs = self.retrieve_python_code(query_embedding, user_id=user_id, topic=topic)
                nb_docs = self.retrieve_notebook_code(query_embedding, user_id=user_id, topic=topic)
                stats["candidates_retrieved"]["student_code_py"] = len(py_docs)
                stats["candidates_retrieved"]["student_code_ipynb"] = len(nb_docs)
                candidates.extend(py_docs)
                candidates.extend(nb_docs)

            if not candidates:
                logger.info("No candidates retrieved for question intent=%s.", intent)
                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": stats,
                }

            # ---- 6. Similarity threshold ----------------------------------
            filtered = self.apply_similarity_threshold(candidates)
            stats["after_similarity_threshold"] = len(filtered)

            if not filtered:
                logger.info(
                    "All %d candidates fell below similarity_threshold=%.2f.",
                    len(candidates), self.config.similarity_threshold,
                )
                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": stats,
                }

            # ---- 7. Deduplication --------------------------------------
            deduped = self.deduplicate_documents(filtered)
            stats["after_dedup"] = len(deduped)

            # ---- 8. Reranking --------------------------------------------
            reranked = self.rerank_documents(deduped, intent=intent, topic=topic, difficulty=difficulty)

            # ---- 9. Balanced, category-aware final selection --------------
            selected = self.select_balanced_context(
                reranked,
                intent=intent,
                max_chunks=effective_max_chunks,
            )
            stats["final_chunk_count"] = len(selected)

            # ---- 10. Context formatting (respects max_context_characters) --
            context_text = self.format_documents(selected)

            # ---- 11. Source tracking ---------------------------------------
            sources = []
            for doc in selected:
                meta = doc.get("metadata", {}) or {}
                sources.append({
                    "id": doc.get("id"),
                    "source": meta.get("source") or meta.get("filename") or meta.get("title"),
                    "topic": meta.get("topic"),
                    "content_type": meta.get("content_type"),
                    "difficulty": meta.get("difficulty"),
                    "file_type": meta.get("file_type"),
                    "user_id": meta.get("user_id"),
                    "similarity": round(doc.get("similarity", 0.0), 4),
                })

            return {
                "context": context_text,
                "documents": selected,
                "intent": intent,
                "sources": sources,
                "retrieval_stats": stats,
            }

        except RAGConnectionError as exc:
            logger.error("Database unavailable during retrieval: %s", exc)
            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {**stats, "errors": ["database_unavailable"]},
            }
        except Exception as exc:  # last-resort safety net — never crash the app
            logger.exception("Unexpected error during retrieve_context: %s", exc)
            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {**stats, "errors": [f"unexpected:{type(exc).__name__}"]},
            }


# ==========================================================================
# Module-level convenience API (what coach.py is expected to import)
# ==========================================================================
_default_rag_instance: Optional[DSA_RAG] = None


def get_default_rag_instance() -> DSA_RAG:
    """Lazily create (once) and return a shared DSA_RAG instance, so the
    embedding model is loaded only once per process."""
    global _default_rag_instance
    if _default_rag_instance is None:
        _default_rag_instance = DSA_RAG()
    return _default_rag_instance


def retrieve_context(
    question: str,
    mode: str = "general",
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    user_id: Optional[str] = None,
    include_code: bool = False,
    k: Optional[int] = None,
    include_leetcode: bool = True,
    include_stories: bool = True,
) -> Dict[str, Any]:
    """Simple functional entry point for coach.py:

        from rag import retrieve_context
        result = retrieve_context("Give me a medium sliding window problem.",
                                   mode="practice")
        print(result["context"])

    See the module docstring for the full parameter and return-value
    documentation.
    """
    rag = get_default_rag_instance()
    return rag.retrieve_context(
        question=question,
        mode=mode,
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=include_code,
        k=k,
        include_leetcode=include_leetcode,
        include_stories=include_stories,
    )


# ==========================================================================
# Manual smoke test (only runs when executing this file directly)
# ==========================================================================
if __name__ == "__main__":  # pragma: no cover
    logging.getLogger("dsa_coach.rag").setLevel(logging.INFO)

    demo_questions = [
        ("What is a stack?", "learn"),
        ("Explain binary search using a real-world analogy.", "story"),
        ("Give me a medium sliding window problem.", "practice"),
        ("Can you give me a hint for Two Sum?", "hint"),
        ("Why is my code giving TLE?", "debug"),
    ]

    for q, m in demo_questions:
        print(f"\n--- mode={m!r} question={q!r} ---")
        try:
            result = retrieve_context(q, mode=m, user_id="demo_user_1")
            print("intent:", result["intent"])
            print("stats:", result["retrieval_stats"])
            print("context preview:", result["context"][:300], "...")
        except Exception as e:
            print("Smoke test failed (expected if no DB is configured):", e)
