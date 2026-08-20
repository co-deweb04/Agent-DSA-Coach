"""
================================================================================
rag.py — Retrieval-Augmented Generation layer for the DSA Coach Agent
================================================================================

PURPOSE
-------
This module is the RETRIEVAL layer of the DSA Coach Agent.

It:
    1. Detects the student's intent.
    2. Embeds the student's question.
    3. Retrieves relevant chunks from PostgreSQL + pgvector.
    4. Filters and reranks candidates.
    5. Balances different content categories.
    6. Builds a clean context for coach.py.

It does NOT call an LLM.

DATABASE
--------
rag_chunks:
    id          SERIAL PRIMARY KEY
    content     TEXT NOT NULL
    metadata    JSONB
    embedding   VECTOR(384)

EMBEDDING MODEL
---------------
BAAI/bge-small-en-v1.5
384-dimensional embeddings.

Student code is always filtered using user_id.

================================================================================
"""

from __future__ import annotations

import os
import re
import json
import hashlib
import logging

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from config import (
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
)


# =============================================================================
# OPTIONAL DEPENDENCIES
# =============================================================================

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


# =============================================================================
# LOGGING
# =============================================================================

logger = logging.getLogger("dsa_coach.rag")

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        )
    )
    logger.addHandler(handler)

logger.setLevel(
    os.environ.get("RAG_LOG_LEVEL", "INFO")
)


# =============================================================================
# CONSTANTS
# =============================================================================

EMBEDDING_MODEL_NAME = EMBEDDING_MODEL
EMBEDDING_DIM = EMBEDDING_DIMENSION

BGE_QUERY_INSTRUCTION = (
    "Represent this sentence for searching relevant passages: "
)

VALID_CONTENT_TYPES = {
    "dsa",
    "story",
    "description",
    "leetcode",
    "student_code",
}

VALID_DIFFICULTIES = {
    "easy",
    "medium",
    "hard",
}

VALID_MODES = {
    "general",
    "learn",
    "story",
    "practice",
    "hint",
    "solution",
    "code_review",
    "debug",
}

INTENTS = {
    "LEARN",
    "EXPLAIN",
    "STORY",
    "HINT",
    "PRACTICE",
    "SOLUTION",
    "CODE_REVIEW",
    "DEBUG",
    "COMPLEXITY",
    "LEETCODE",
    "GENERAL",
}


# =============================================================================
# MODE → INTENT
# =============================================================================

MODE_TO_INTENT = {
    "general": None,
    "learn": "LEARN",
    "story": "STORY",
    "practice": "PRACTICE",
    "hint": "HINT",
    "solution": "SOLUTION",
    "code_review": "CODE_REVIEW",
    "debug": "DEBUG",
}


# =============================================================================
# RAG CONFIGURATION
# =============================================================================

@dataclass
class RAGConfig:
    """
    Central configuration for the retrieval system.

    Database and embedding settings come from config.py.
    Retrieval-specific settings are kept here.
    """

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    db_host: str = DB_HOST
    db_port: str = DB_PORT
    db_name: str = DB_NAME
    db_user: str = DB_USER
    db_password: str = DB_PASSWORD

    # -------------------------------------------------------------------------
    # Embedding
    # -------------------------------------------------------------------------

    embedding_model_name: str = EMBEDDING_MODEL_NAME

    # -------------------------------------------------------------------------
    # Retrieval
    # -------------------------------------------------------------------------

    candidate_k: int = 18
    max_context_chunks: int = 8
    max_context_characters: int = 12000

    # -------------------------------------------------------------------------
    # Similarity
    # -------------------------------------------------------------------------

    similarity_threshold: float = 0.60

    # -------------------------------------------------------------------------
    # Reranking weights
    # -------------------------------------------------------------------------

    weight_similarity: float = 0.55
    weight_topic_match: float = 0.20
    weight_difficulty_match: float = 0.10
    weight_content_type_relevance: float = 0.10
    weight_intent_match: float = 0.05


# =============================================================================
# INTENT → CATEGORY PLAN
# =============================================================================

INTENT_CATEGORY_PLAN: Dict[str, Dict[str, int]] = {

    "LEARN": {
        "dsa": 2,
        "description": 1,
        "story": 1,
    },

    "EXPLAIN": {
        "dsa": 2,
        "description": 1,
    },

    "STORY": {
        "story": 2,
        "description": 1,
        "dsa": 1,
    },

    "HINT": {
        "dsa": 1,
        "leetcode": 1,
        "description": 1,
    },

    "PRACTICE": {
        "leetcode": 5,
        "dsa": 1,
    },

    "LEETCODE": {
        "leetcode": 5,
        "dsa": 1,
    },

    "SOLUTION": {
        "dsa": 2,
        "leetcode": 1,
        "description": 1,
    },

    "CODE_REVIEW": {
        "student_code": 3,
        "dsa": 2,
        "description": 1,
    },

    "DEBUG": {
        "student_code": 3,
        "dsa": 2,
        "description": 1,
    },

    "COMPLEXITY": {
        "dsa": 2,
        "description": 2,
    },

    "GENERAL": {
        "dsa": 1,
        "description": 1,
        "story": 1,
        "leetcode": 1,
    },
}


# =============================================================================
# INTENT → ACTIVE CATEGORIES
# =============================================================================

INTENT_ACTIVE_CATEGORIES: Dict[str, set] = {

    "LEARN": {
        "dsa",
        "description",
        "story",
    },

    "EXPLAIN": {
        "dsa",
        "description",
    },

    "STORY": {
        "story",
        "description",
        "dsa",
    },

    "HINT": {
        "dsa",
        "leetcode",
        "description",
    },

    "PRACTICE": {
        "leetcode",
        "dsa",
    },

    "LEETCODE": {
        "leetcode",
        "dsa",
    },

    "SOLUTION": {
        "dsa",
        "leetcode",
        "description",
    },

    "CODE_REVIEW": {
        "student_code",
        "dsa",
        "description",
    },

    "DEBUG": {
        "student_code",
        "dsa",
        "description",
    },

    "COMPLEXITY": {
        "dsa",
        "description",
    },

    "GENERAL": {
        "dsa",
        "description",
        "story",
        "leetcode",
    },
}


# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================

class RAGError(Exception):
    """Base class for recoverable RAG errors."""


class RAGConnectionError(RAGError):
    """Raised when PostgreSQL cannot be reached."""


class RAGEmbeddingError(RAGError):
    """Raised when embedding creation fails."""


# =============================================================================
# MAIN RAG CLASS
# =============================================================================

class DSA_RAG:

    def __init__(self, config: Optional[RAGConfig] = None):

        self.config = config or RAGConfig()

        # Lazy loading prevents the embedding model from loading
        # unnecessarily during application startup.
        self._embedding_model = None

    # =========================================================================
    # EMBEDDING MODEL
    # =========================================================================

    def _load_embedding_model(self):

        if self._embedding_model is not None:
            return self._embedding_model

        if SentenceTransformer is None:
            raise RAGEmbeddingError(
                "sentence-transformers is not installed. "
                "Install it using: pip install sentence-transformers"
            )

        try:

            logger.info(
                "Loading embedding model: %s",
                self.config.embedding_model_name,
            )

            self._embedding_model = SentenceTransformer(
                self.config.embedding_model_name
            )

        except Exception as exc:

            raise RAGEmbeddingError(
                f"Failed to load embedding model: {exc}"
            ) from exc

        return self._embedding_model

    # =========================================================================
    # CREATE QUERY EMBEDDING
    # =========================================================================

    def create_query_embedding(
        self,
        text: str,
    ) -> List[float]:

        if not text or not text.strip():
            raise RAGEmbeddingError(
                "Cannot embed an empty query."
            )

        model = self._load_embedding_model()

        try:

            prefixed_query = (
                f"{BGE_QUERY_INSTRUCTION}{text.strip()}"
            )

            vector = model.encode(
                prefixed_query,
                normalize_embeddings=True,
            )

            vector = [float(x) for x in vector]

            if len(vector) != EMBEDDING_DIM:
                raise RAGEmbeddingError(
                    f"Expected embedding dimension {EMBEDDING_DIM}, "
                    f"but received {len(vector)}."
                )

            return vector

        except RAGEmbeddingError:
            raise

        except Exception as exc:

            raise RAGEmbeddingError(
                f"Failed to embed query: {exc}"
            ) from exc

    # =========================================================================
    # DATABASE CONNECTION
    # =========================================================================

    def get_connection(self):

        if psycopg2 is None:
            raise RAGConnectionError(
                "psycopg2 is not installed. "
                "Install it using: pip install psycopg2-binary"
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

            logger.error(
                "Database connection failed "
                "(host=%s, db=%s, user=%s): %s",
                cfg.db_host,
                cfg.db_name,
                cfg.db_user,
                type(exc).__name__,
            )

            raise RAGConnectionError(
                "Could not connect to the database."
            ) from exc

    # =========================================================================
    # INTENT DETECTION
    # =========================================================================

    @staticmethod
    def detect_intent(question: str) -> str:

        q = (question or "").lower().strip()

        if not q:
            return "GENERAL"

        rules = [

            # ---------------------------------------------------------------
            # DEBUG
            # ---------------------------------------------------------------

            (
                "DEBUG",
                [
                    r"\btle\b",
                    r"time limit exceeded",
                    r"wrong answer",
                    r"\bbug\b",
                    r"\berror\b",
                    r"not working",
                    r"\bdebug\b",
                    r"\bfails?\b",
                    r"runtime error",
                    r"segmentation fault",
                    r"exception",
                    r"stack trace",
                    r"traceback",
                ],
            ),

            # ---------------------------------------------------------------
            # CODE REVIEW
            # ---------------------------------------------------------------

            (
                "CODE_REVIEW",
                [
                    r"review my code",
                    r"review this code",
                    r"code review",
                    r"feedback on my code",
                    r"check my code",
                    r"improve my code",
                    r"critique my (code|solution)",
                ],
            ),

            # ---------------------------------------------------------------
            # COMPLEXITY
            # ---------------------------------------------------------------

            (
                "COMPLEXITY",
                [
                    r"time complexity",
                    r"space complexity",
                    r"big[\s-]?o",
                    r"complexity of",
                    r"how efficient",
                ],
            ),

            # ---------------------------------------------------------------
            # SOLUTION
            # ---------------------------------------------------------------

            (
                "SOLUTION",
                [
                    r"\bsolution\b",
                    r"solve this",
                    r"full solution",
                    r"complete solution",
                    r"answer to this problem",
                    r"give me the answer",
                ],
            ),

            # ---------------------------------------------------------------
            # HINT
            # ---------------------------------------------------------------

            (
                "HINT",
                [
                    r"\bhint\b",
                    r"i'?m stuck",
                    r"nudge me",
                    r"small clue",
                    r"point me in the right direction",
                ],
            ),

            # ---------------------------------------------------------------
            # LEETCODE / PRACTICE
            # ---------------------------------------------------------------

            (
                "LEETCODE",
                [
                    r"leetcode",
                    r"practice problem",
                    r"give me a problem",
                    r"easy problem",
                    r"medium problem",
                    r"hard problem",
                    r"coding problem",
                    r"practice question",
                    r"another problem",
                ],
            ),

            # ---------------------------------------------------------------
            # STORY
            # ---------------------------------------------------------------

            (
                "STORY",
                [
                    r"\bstory\b",
                    r"analogy",
                    r"real[\s-]?world",
                    r"like i'?m 5",
                    r"\beli5\b",
                    r"simple explanation",
                    r"beginner explanation",
                    r"explain .* using",
                ],
            ),

            # ---------------------------------------------------------------
            # EXPLAIN
            # ---------------------------------------------------------------

            (
                "EXPLAIN",
                [
                    r"^explain\b",
                    r"how does",
                    r"how do",
                    r"^why\b",
                    r"walk me through",
                ],
            ),

            # ---------------------------------------------------------------
            # LEARN
            # ---------------------------------------------------------------

            (
                "LEARN",
                [
                    r"^what is\b",
                    r"^what's\b",
                    r"\bdefine\b",
                    r"definition of",
                    r"learn about",
                    r"introduce",
                    r"tell me about",
                ],
            ),
        ]

        for intent, patterns in rules:

            for pattern in patterns:

                if re.search(pattern, q):
                    return intent

        return "GENERAL"

    # =========================================================================
    # SEMANTIC SEARCH
    # =========================================================================

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

        limit = limit or self.config.candidate_k

        vector_literal = (
            "["
            + ",".join(
                repr(float(x))
                for x in query_embedding
            )
            + "]"
        )

        where_clauses = [
            "embedding IS NOT NULL"
        ]

        params: List[Any] = []

        # ---------------------------------------------------------------------
        # Content type
        # ---------------------------------------------------------------------

        if content_type:

            where_clauses.append(
                "metadata->>'content_type' = %s"
            )

            params.append(content_type)

        # ---------------------------------------------------------------------
        # Topic
        # ---------------------------------------------------------------------

        if topic:

            where_clauses.append(
                "LOWER(metadata->>'topic') = LOWER(%s)"
            )

            params.append(topic)

        # ---------------------------------------------------------------------
        # Difficulty
        # ---------------------------------------------------------------------

        if difficulty:

            where_clauses.append(
                "LOWER(metadata->>'difficulty') = LOWER(%s)"
            )

            params.append(difficulty)

        # ---------------------------------------------------------------------
        # File type
        # ---------------------------------------------------------------------

        if file_type:

            where_clauses.append(
                "metadata->>'file_type' = %s"
            )

            params.append(file_type)

        # ---------------------------------------------------------------------
        # User isolation
        # ---------------------------------------------------------------------

        if user_id is not None:

            where_clauses.append(
                "metadata->>'user_id' = %s"
            )

            params.append(str(user_id))

        where_sql = " AND ".join(where_clauses)

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

        query_params = [
            vector_literal,
            *params,
            vector_literal,
            limit,
        ]

        try:

            conn = self.get_connection()

        except RAGConnectionError:

            logger.error(
                "semantic_search aborted: "
                "database connection unavailable."
            )

            return []

        try:

            with conn:

                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as cursor:

                    cursor.execute(
                        sql,
                        query_params,
                    )

                    rows = cursor.fetchall()

        except Exception as exc:

            logger.error(
                "semantic_search query failed: %s",
                type(exc).__name__,
            )

            return []

        finally:

            try:
                conn.close()
            except Exception:
                pass

        results = []

        for row in rows:

            metadata = row.get("metadata") or {}

            if isinstance(metadata, str):

                try:
                    metadata = json.loads(metadata)

                except (
                    json.JSONDecodeError,
                    TypeError,
                ):
                    metadata = {}

            results.append(
                {
                    "id": row.get("id"),
                    "content": row.get("content") or "",
                    "metadata": metadata,
                    "similarity": float(
                        row.get("similarity") or 0.0
                    ),
                }
            )

        return results

    # =========================================================================
    # CATEGORY RETRIEVAL
    # =========================================================================

    def retrieve_dsa_knowledge(
        self,
        query_embedding,
        topic=None,
        limit=None,
    ):

        return self.semantic_search(
            query_embedding,
            content_type="dsa",
            topic=topic,
            limit=limit,
        )

    def retrieve_stories(
        self,
        query_embedding,
        topic=None,
        limit=None,
    ):

        return self.semantic_search(
            query_embedding,
            content_type="story",
            topic=topic,
            limit=limit,
        )

    def retrieve_descriptions(
        self,
        query_embedding,
        topic=None,
        limit=None,
    ):

        return self.semantic_search(
            query_embedding,
            content_type="description",
            topic=topic,
            limit=limit,
        )

    def retrieve_leetcode(
        self,
        query_embedding,
        topic=None,
        difficulty=None,
        limit=None,
    ):

        return self.semantic_search(
            query_embedding,
            content_type="leetcode",
            topic=topic,
            difficulty=difficulty,
            limit=limit,
        )

    def retrieve_python_code(
        self,
        query_embedding,
        user_id,
        topic=None,
        limit=None,
    ):

        if not user_id:

            logger.warning(
                "Python code retrieval skipped: "
                "user_id missing."
            )

            return []

        return self.semantic_search(
            query_embedding,
            content_type="student_code",
            file_type="py",
            user_id=user_id,
            topic=topic,
            limit=limit,
        )

    def retrieve_notebook_code(
        self,
        query_embedding,
        user_id,
        topic=None,
        limit=None,
    ):

        if not user_id:

            logger.warning(
                "Notebook retrieval skipped: "
                "user_id missing."
            )

            return []

        return self.semantic_search(
            query_embedding,
            content_type="student_code",
            file_type="ipynb",
            user_id=user_id,
            topic=topic,
            limit=limit,
        )

    # =========================================================================
    # SIMILARITY FILTER
    # =========================================================================

    def apply_similarity_threshold(
        self,
        documents: List[Dict[str, Any]],
        threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:

        threshold = (
            self.config.similarity_threshold
            if threshold is None
            else threshold
        )

        return [
            document
            for document in documents
            if document.get("similarity", 0.0) >= threshold
        ]

    # =========================================================================
    # DEDUPLICATION
    # =========================================================================

    @staticmethod
    def deduplicate_documents(
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        seen_ids = set()
        seen_hashes = set()

        deduped = []

        for document in documents:

            document_id = document.get("id")

            if document_id is not None:

                if document_id in seen_ids:
                    continue

                seen_ids.add(document_id)

            content = (
                document.get("content") or ""
            ).strip()

            content_hash = hashlib.md5(
                content.encode("utf-8")
            ).hexdigest()

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(content_hash)

            deduped.append(document)

        return deduped

    # =========================================================================
    # RERANKING
    # =========================================================================

    def rerank_documents(
        self,
        documents: List[Dict[str, Any]],
        intent: str,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        cfg = self.config

        active_categories = (
            INTENT_ACTIVE_CATEGORIES.get(
                intent,
                set(),
            )
        )

        category_plan = (
            INTENT_CATEGORY_PLAN.get(
                intent,
                {},
            )
        )

        max_plan_weight = (
            max(category_plan.values())
            if category_plan
            else 1
        )

        scored = []

        for document in documents:

            metadata = (
                document.get("metadata")
                or {}
            )

            similarity = float(
                document.get("similarity", 0.0)
            )

            # -----------------------------------------------------------------
            # Topic match
            # -----------------------------------------------------------------

            topic_match = 0.0

            if (
                topic
                and str(
                    metadata.get("topic", "")
                ).lower()
                == str(topic).lower()
            ):
                topic_match = 1.0

            # -----------------------------------------------------------------
            # Difficulty match
            # -----------------------------------------------------------------

            difficulty_match = 0.0

            if (
                difficulty
                and str(
                    metadata.get("difficulty", "")
                ).lower()
                == str(difficulty).lower()
            ):
                difficulty_match = 1.0

            # -----------------------------------------------------------------
            # Content type relevance
            # -----------------------------------------------------------------

            content_type = metadata.get(
                "content_type",
                "",
            )

            content_type_relevance = (
                category_plan.get(
                    content_type,
                    0,
                )
                / max_plan_weight
                if category_plan
                else 0.0
            )

            # -----------------------------------------------------------------
            # Intent match
            # -----------------------------------------------------------------

            intent_match = (
                1.0
                if content_type in active_categories
                else 0.0
            )

            # -----------------------------------------------------------------
            # Final score
            # -----------------------------------------------------------------

            score = (
                cfg.weight_similarity * similarity
                + cfg.weight_topic_match * topic_match
                + cfg.weight_difficulty_match * difficulty_match
                + cfg.weight_content_type_relevance
                * content_type_relevance
                + cfg.weight_intent_match
                * intent_match
            )

            updated_document = dict(document)

            updated_document[
                "rerank_score"
            ] = score

            scored.append(updated_document)

        scored.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        return scored

    # =========================================================================
    # BALANCED CONTEXT SELECTION
    # =========================================================================

    def select_balanced_context(
        self,
        documents: List[Dict[str, Any]],
        intent: str,
        max_chunks: Optional[int] = None,
    ) -> List[Dict[str, Any]]:

        max_chunks = (
            max_chunks
            if max_chunks is not None
            else self.config.max_context_chunks
        )

        plan = INTENT_CATEGORY_PLAN.get(
            intent,
            {},
        )

        by_category: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

        for document in documents:

            content_type = (
                document
                .get("metadata", {})
                .get("content_type", "unknown")
            )

            by_category.setdefault(
                content_type,
                []
            ).append(document)

        selected = []
        selected_ids = set()

        # ---------------------------------------------------------------------
        # Pass 1: category quotas
        # ---------------------------------------------------------------------

        for content_type, quota in plan.items():

            for document in by_category.get(
                content_type,
                []
            )[:quota]:

                if len(selected) >= max_chunks:
                    break

                key = (
                    document.get("id")
                    if document.get("id") is not None
                    else id(document)
                )

                if key in selected_ids:
                    continue

                selected.append(document)
                selected_ids.add(key)

        # ---------------------------------------------------------------------
        # Pass 2: fill remaining slots
        # ---------------------------------------------------------------------

        if len(selected) < max_chunks:

            for document in documents:

                if len(selected) >= max_chunks:
                    break

                key = (
                    document.get("id")
                    if document.get("id") is not None
                    else id(document)
                )

                if key in selected_ids:
                    continue

                selected.append(document)
                selected_ids.add(key)

        return selected[:max_chunks]

    # =========================================================================
    # FORMAT CONTEXT
    # =========================================================================

    def format_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> str:

        max_chars = (
            self.config.max_context_characters
        )

        section_titles = {

            "dsa":
                "DSA KNOWLEDGE",

            "description":
                "DESCRIPTION",

            "story":
                "STORY",

            "leetcode":
                "LEETCODE",

            "student_code":
                "STUDENT CODE",
        }

        grouped: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

        for document in documents:

            content_type = (
                document
                .get("metadata", {})
                .get("content_type", "unknown")
            )

            grouped.setdefault(
                content_type,
                []
            ).append(document)

        pieces = []

        total_length = 0
        truncated = False

        for content_type, docs in grouped.items():

            title = section_titles.get(
                content_type,
                content_type.upper(),
            )

            for document in docs:

                metadata = (
                    document.get("metadata")
                    or {}
                )

                header_lines = [
                    f"===== {title} ====="
                ]

                # -------------------------------------------------------------
                # LeetCode
                # -------------------------------------------------------------

                if content_type == "leetcode":

                    if metadata.get("title"):
                        header_lines.append(
                            f"Title: {metadata['title']}"
                        )

                    if metadata.get("difficulty"):
                        header_lines.append(
                            f"Difficulty: "
                            f"{metadata['difficulty']}"
                        )

                    if metadata.get("topic"):
                        header_lines.append(
                            f"Topic: "
                            f"{metadata['topic']}"
                        )

                # -------------------------------------------------------------
                # Student code
                # -------------------------------------------------------------

                elif content_type == "student_code":

                    if metadata.get("filename"):
                        header_lines.append(
                            f"Filename: "
                            f"{metadata['filename']}"
                        )

                    if metadata.get("file_type"):
                        header_lines.append(
                            f"File Type: "
                            f"{metadata['file_type']}"
                        )

                    if metadata.get("topic"):
                        header_lines.append(
                            f"Topic: "
                            f"{metadata['topic']}"
                        )

                # -------------------------------------------------------------
                # Other content
                # -------------------------------------------------------------

                else:

                    if metadata.get("source"):
                        header_lines.append(
                            f"Source: "
                            f"{metadata['source']}"
                        )

                    if metadata.get("topic"):
                        header_lines.append(
                            f"Topic: "
                            f"{metadata['topic']}"
                        )

                content = (
                    document.get("content")
                    or ""
                ).strip()

                block = (
                    "\n".join(header_lines)
                    + "\n\n"
                    + content
                    + "\n"
                )

                if (
                    total_length
                    + len(block)
                    > max_chars
                ):

                    truncated = True
                    break

                pieces.append(block)

                total_length += len(block)

            if truncated:
                break

        context = "\n".join(
            pieces
        ).strip()

        if truncated:

            context += (
                "\n\n"
                "[context truncated at "
                "max_context_characters]"
            )

        return context

    # =========================================================================
    # ACTIVE CATEGORY BUILDER
    # =========================================================================

    def _build_active_categories(
        self,
        intent: str,
        include_code: bool,
        include_leetcode: bool,
        include_stories: bool,
        user_id: Optional[str],
    ) -> set:

        categories = set(
            INTENT_ACTIVE_CATEGORIES.get(
                intent,
                {
                    "dsa",
                    "description",
                },
            )
        )

        # ---------------------------------------------------------------------
        # LeetCode
        # ---------------------------------------------------------------------

        if not include_leetcode:
            categories.discard("leetcode")

        # ---------------------------------------------------------------------
        # Stories
        # ---------------------------------------------------------------------

        if not include_stories:
            categories.discard("story")

        # ---------------------------------------------------------------------
        # Student code
        # ---------------------------------------------------------------------

        wants_code = (
            include_code
            or intent in (
                "CODE_REVIEW",
                "DEBUG",
            )
        )

        if wants_code and user_id:
            categories.add("student_code")
        else:
            categories.discard("student_code")

        return categories

    # =========================================================================
    # MAIN RETRIEVAL METHOD
    # =========================================================================

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

        stats = {
            "candidates_retrieved": {},
            "after_similarity_threshold": 0,
            "after_dedup": 0,
            "final_chunk_count": 0,
            "errors": [],
        }

        # =========================================================================
        # 1. INPUT VALIDATION
        # =========================================================================

        if not question or not question.strip():

            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {
                    **stats,
                    "errors": [
                        "empty_query"
                    ],
                },
            }

        mode = (
            mode or ""
        ).strip().lower()

        if mode not in VALID_MODES:

            logger.warning(
                "Unknown mode '%s'. "
                "Using general mode.",
                mode,
            )

            mode = "general"

        if (
            difficulty
            and difficulty.lower()
            not in VALID_DIFFICULTIES
        ):

            logger.warning(
                "Unknown difficulty '%s'. "
                "Ignoring filter.",
                difficulty,
            )

            difficulty = None

        # `k` overrides max_context_chunks
        # only for this request.

        if k is not None:

            try:

                effective_max_chunks = (
                    int(k)
                    if int(k) > 0
                    else self.config.max_context_chunks
                )

            except (TypeError, ValueError):

                effective_max_chunks = (
                    self.config.max_context_chunks
                )

        else:

            effective_max_chunks = (
                self.config.max_context_chunks
            )

        try:

            # =========================================================================
            # 2. INTENT
            # =========================================================================

            mapped_intent = MODE_TO_INTENT.get(
                mode
            )

            intent = (
                mapped_intent
                or self.detect_intent(question)
            )

            # =========================================================================
            # 3. EMBEDDING
            # =========================================================================

            try:

                query_embedding = (
                    self.create_query_embedding(
                        question
                    )
                )

            except RAGEmbeddingError as exc:

                logger.error(
                    "Embedding failed: %s",
                    exc,
                )

                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": {
                        **stats,
                        "errors": [
                            "embedding_failed"
                        ],
                    },
                }

            # =========================================================================
            # 4. ACTIVE CATEGORIES
            # =========================================================================

            active_categories = (
                self._build_active_categories(
                    intent=intent,
                    include_code=include_code,
                    include_leetcode=include_leetcode,
                    include_stories=include_stories,
                    user_id=user_id,
                )
            )

            # =========================================================================
            # 5. RETRIEVE CANDIDATES
            # =========================================================================

            candidates = []

            # -------------------------------------------------------------------------
            # DSA
            # -------------------------------------------------------------------------

            if "dsa" in active_categories:

                docs = self.retrieve_dsa_knowledge(
                    query_embedding,
                    topic=topic,
                )

                stats[
                    "candidates_retrieved"
                ]["dsa"] = len(docs)

                candidates.extend(docs)

            # -------------------------------------------------------------------------
            # DESCRIPTION
            # -------------------------------------------------------------------------

            if "description" in active_categories:

                docs = self.retrieve_descriptions(
                    query_embedding,
                    topic=topic,
                )

                stats[
                    "candidates_retrieved"
                ]["description"] = len(docs)

                candidates.extend(docs)

            # -------------------------------------------------------------------------
            # STORY
            # -------------------------------------------------------------------------

            if "story" in active_categories:

                docs = self.retrieve_stories(
                    query_embedding,
                    topic=topic,
                )

                stats[
                    "candidates_retrieved"
                ]["story"] = len(docs)

                candidates.extend(docs)

            # -------------------------------------------------------------------------
            # LEETCODE
            # -------------------------------------------------------------------------

            if "leetcode" in active_categories:

                docs = self.retrieve_leetcode(
                    query_embedding,
                    topic=topic,
                    difficulty=difficulty,
                )

                stats[
                    "candidates_retrieved"
                ]["leetcode"] = len(docs)

                candidates.extend(docs)

            # -------------------------------------------------------------------------
            # STUDENT PYTHON / NOTEBOOK CODE
            # -------------------------------------------------------------------------

            if (
                "student_code"
                in active_categories
                and user_id
            ):

                python_docs = (
                    self.retrieve_python_code(
                        query_embedding,
                        user_id=user_id,
                        topic=topic,
                    )
                )

                notebook_docs = (
                    self.retrieve_notebook_code(
                        query_embedding,
                        user_id=user_id,
                        topic=topic,
                    )
                )

                stats[
                    "candidates_retrieved"
                ]["student_code_py"] = len(
                    python_docs
                )

                stats[
                    "candidates_retrieved"
                ]["student_code_ipynb"] = len(
                    notebook_docs
                )

                candidates.extend(
                    python_docs
                )

                candidates.extend(
                    notebook_docs
                )

            # =========================================================================
            # NO CANDIDATES
            # =========================================================================

            if not candidates:

                logger.info(
                    "No candidates retrieved "
                    "for intent=%s.",
                    intent,
                )

                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": stats,
                }

            # =========================================================================
            # 6. SIMILARITY FILTER
            # =========================================================================

            filtered = (
                self.apply_similarity_threshold(
                    candidates
                )
            )

            stats[
                "after_similarity_threshold"
            ] = len(filtered)

            if not filtered:

                logger.info(
                    "All candidates fell below "
                    "similarity threshold %.2f.",
                    self.config.similarity_threshold,
                )

                return {
                    "context": "",
                    "documents": [],
                    "intent": intent,
                    "sources": [],
                    "retrieval_stats": stats,
                }

            # =========================================================================
            # 7. DEDUPLICATION
            # =========================================================================

            deduped = (
                self.deduplicate_documents(
                    filtered
                )
            )

            stats["after_dedup"] = len(
                deduped
            )

            # =========================================================================
            # 8. RERANK
            # =========================================================================

            reranked = (
                self.rerank_documents(
                    deduped,
                    intent=intent,
                    topic=topic,
                    difficulty=difficulty,
                )
            )

            # =========================================================================
            # 9. BALANCED SELECTION
            # =========================================================================

            selected = (
                self.select_balanced_context(
                    reranked,
                    intent=intent,
                    max_chunks=effective_max_chunks,
                )
            )

            stats[
                "final_chunk_count"
            ] = len(selected)

            # =========================================================================
            # 10. FORMAT CONTEXT
            # =========================================================================

            context_text = (
                self.format_documents(
                    selected
                )
            )

            # =========================================================================
            # 11. SOURCE TRACKING
            # =========================================================================

            sources = []

            for document in selected:

                metadata = (
                    document.get("metadata")
                    or {}
                )

                sources.append(
                    {
                        "id":
                            document.get("id"),

                        "source":
                            metadata.get("source")
                            or metadata.get("filename")
                            or metadata.get("title"),

                        "topic":
                            metadata.get("topic"),

                        "content_type":
                            metadata.get(
                                "content_type"
                            ),

                        "difficulty":
                            metadata.get(
                                "difficulty"
                            ),

                        "file_type":
                            metadata.get(
                                "file_type"
                            ),

                        "user_id":
                            metadata.get(
                                "user_id"
                            ),

                        "similarity":
                            round(
                                document.get(
                                    "similarity",
                                    0.0,
                                ),
                                4,
                            ),
                    }
                )

            # =========================================================================
            # FINAL RESULT
            # =========================================================================

            return {
                "context": context_text,
                "documents": selected,
                "intent": intent,
                "sources": sources,
                "retrieval_stats": stats,
            }

        # =========================================================================
        # DATABASE ERROR
        # =========================================================================

        except RAGConnectionError as exc:

            logger.error(
                "Database unavailable: %s",
                exc,
            )

            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {
                    **stats,
                    "errors": [
                        "database_unavailable"
                    ],
                },
            }

        # =========================================================================
        # UNEXPECTED ERROR
        # =========================================================================

        except Exception as exc:

            logger.exception(
                "Unexpected RAG error: %s",
                exc,
            )

            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {
                    **stats,
                    "errors": [
                        f"unexpected:{type(exc).__name__}"
                    ],
                },
            }


# =============================================================================
# MODULE-LEVEL DEFAULT INSTANCE
# =============================================================================

_default_rag_instance: Optional[
    DSA_RAG
] = None


def get_default_rag_instance() -> DSA_RAG:

    global _default_rag_instance

    if _default_rag_instance is None:

        _default_rag_instance = DSA_RAG()

    return _default_rag_instance


# =============================================================================
# PUBLIC FUNCTION
# =============================================================================

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


# =============================================================================
# MANUAL SMOKE TEST
# =============================================================================

if __name__ == "__main__":

    logging.getLogger(
        "dsa_coach.rag"
    ).setLevel(logging.INFO)

    demo_questions = [

        (
            "What is a stack?",
            "learn",
        ),

        (
            "Explain binary search using a real-world analogy.",
            "story",
        ),

        (
            "Give me a medium sliding window problem.",
            "practice",
        ),

        (
            "Can you give me a hint for Two Sum?",
            "hint",
        ),

        (
            "Why is my code giving TLE?",
            "debug",
        ),
    ]

    for question, mode in demo_questions:

        print(
            f"\n--- mode={mode!r} "
            f"question={question!r} ---"
        )

        try:

            result = retrieve_context(
                question,
                mode=mode,
                user_id="demo_user_1",
            )

            print(
                "intent:",
                result["intent"],
            )

            print(
                "stats:",
                result["retrieval_stats"],
            )

            print(
                "context preview:",
                result["context"][:300],
                "...",
            )

        except Exception as exc:

            print(
                "Smoke test failed "
                "(expected if DB is not configured):",
                exc,
            )