# state.py

from typing import TypedDict, List, Optional


class AgentState(TypedDict, total=False):

    # User input
    question: str
    mode: str

    # DSA filters
    topic: Optional[str]
    difficulty: Optional[str]

    # User information
    user_id: Optional[str]
    student_code: Optional[str]

    # Agent routing
    intent: str

    # RAG
    context: str

    # Agent processing
    plan: str
    draft_response: str

    # Critic
    critique: str
    needs_retry: bool

    # Agent loop
    loop_count: int

    # Conversation
    history: List[str]

    # Final answer
    final_response: str