# agents/code_review_agent.py

from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context


client = genai.Client(api_key=GEMINI_API_KEY)


def code_review_agent(state):

    question = state.get("question", "")
    topic = state.get("topic")
    difficulty = state.get("difficulty")
    user_id = state.get("user_id")
    student_code = state.get("student_code")

    if not student_code:
        return {
            "draft_response": (
                "## Code Review\n\n"
                "Please provide your code so I can review it."
            )
        }

    retrieval_question = f"""
Student question:
{question}

Student code:
{student_code}
"""

    result = retrieve_context(
        question=retrieval_question,
        mode="code_review",
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=True,
        include_leetcode=False,
        include_stories=False,
    )

    context = result.get("context", "")

    prompt = f"""
You are the Code Review Agent of a DSA Coach.

Your job is to analyze the student's actual code.

Student question:
{question}

Student code:
```text
{student_code}
"""