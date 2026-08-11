# Truncate the block if necessary to respect the character budget
                    remaining_budget = max_chars - total_len
                    if remaining_budget > 100:
                        pieces.append(block[:remaining_budget] + "\n[Context Truncated]")
                    break

                pieces.append(block)
                total_len += len(block)

            if truncated:
                break

        return "\n".join(pieces).strip()

    # ----------------------------------------------------------------
    # High-level pipeline entrypoint
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
        """Main interface for `coach.py`. Coordinates retrieval, filtering,
        reranking, deduplication, and formatting into a final payload."""
        
        # 1. Input validation & mode normalization
        q = (question or "").strip()
        if not q:
            return {
                "context": "",
                "documents": [],
                "intent": "GENERAL",
                "sources": [],
                "retrieval_stats": {
                    "total_candidates_retrieved": 0,
                    "after_threshold": 0,
                    "after_dedup": 0,
                    "final_selected": 0,
                },
            }

        mode = mode.lower() if mode and mode.lower() in VALID_MODES else "general"
        
        # Backward compatibility override for chunk sizing
        if k is not None and k > 0:
            self.config.max_context_chunks = k

        # 2. Determine intent
        intent = MODE_TO_INTENT.get(mode) or self.detect_intent(q)

        # 3. Create query embedding
        query_embedding = self.create_query_embedding(q)

        # 4. Candidate Retrieval based on intent
        active_categories = set(INTENT_ACTIVE_CATEGORIES.get(intent, VALID_CONTENT_TYPES))
        
        # Respect backward-compatibility flags
        if not include_leetcode and "leetcode" in active_categories:
            active_categories.remove("leetcode")
        if not include_stories and "story" in active_categories:
            active_categories.remove("story")
        if include_code and user_id:
            active_categories.add("student_code")

        candidates: List[Dict[str, Any]] = []

        if "dsa" in active_categories:
            candidates.extend(self.retrieve_dsa_knowledge(query_embedding, topic=topic))
        if "story" in active_categories:
            candidates.extend(self.retrieve_stories(query_embedding, topic=topic))
        if "description" in active_categories:
            candidates.extend(self.retrieve_descriptions(query_embedding, topic=topic))
        if "leetcode" in active_categories:
            candidates.extend(
                self.retrieve_leetcode(query_embedding, topic=topic, difficulty=difficulty)
            )
        if "student_code" in active_categories and user_id:
            candidates.extend(
                self.retrieve_python_code(query_embedding, user_id=user_id, topic=topic)
            )
            candidates.extend(
                self.retrieve_notebook_code(query_embedding, user_id=user_id, topic=topic)
            )

        total_retrieved = len(candidates)

        # 5. Quality Gate: Apply similarity threshold
        filtered = self.apply_similarity_threshold(candidates)
        after_threshold_count = len(filtered)

        # 6. Deduplicate candidates
        deduped = self.deduplicate_documents(filtered)
        after_dedup_count = len(deduped)

        # 7. Rerank remaining candidates
        reranked = self.rerank_documents(
            deduped, intent=intent, topic=topic, difficulty=difficulty
        )

        # 8. Category-balanced selection
        selected_docs = self.select_balanced_context(reranked, intent=intent)

        # 9. Format structured context text
        context_text = self.format_documents(selected_docs)

        # 10. Extract metadata sources
        sources = [
            {
                "id": doc.get("id"),
                "content_type": (doc.get("metadata") or {}).get("content_type"),
                "title": (doc.get("metadata") or {}).get("title"),
                "source": (doc.get("metadata") or {}).get("source"),
                "topic": (doc.get("metadata") or {}).get("topic"),
                "similarity": round(doc.get("similarity", 0.0), 4),
            }
            for doc in selected_docs
        ]

        return {
            "context": context_text,
            "documents": selected_docs,
            "intent": intent,
            "sources": sources,
            "retrieval_stats": {
                "total_candidates_retrieved": total_retrieved,
                "after_threshold": after_threshold_count,
                "after_dedup": after_dedup_count,
                "final_selected": len(selected_docs),
            },
        }


# ==========================================================================
# Module-level instance & public wrapper function
# ==========================================================================
_rag_instance: Optional[DSA_RAG] = None


def get_rag_instance() -> DSA_RAG:
    """Returns a module-level singleton instance of DSA_RAG to prevent
    re-instantiating and re-loading the sentence transformer on every query."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = DSA_RAG()
    return _rag_instance


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
    """Module-level wrapper around the default `DSA_RAG` singleton."""
    rag = get_rag_instance()
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
