# agents/learning_agent.py

from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context


client = genai.Client(api_key=GEMINI_API_KEY)


def learning_agent(state):

    question = state.get("question", "")
    topic = state.get("topic")
    difficulty = state.get("difficulty")
    user_id = state.get("user_id")

    # Retrieve educational context
    result = retrieve_context(
        question=question,
        mode="learn",
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=False,
        include_leetcode=False,
        include_stories=True,
    )

    context = result.get("context", "")

    prompt = f"""
You are the Learning Agent of a DSA Coach.

Your job is to TEACH the student.

Student question:
{question}

Relevant knowledge retrieved from the DSA knowledge base:
{context}

Instructions:

1. Explain the DSA concept clearly.
2. Start with intuition before technical details.
3. Use a simple example when useful.
4. Explain important operations or steps.
5. Include time and space complexity when relevant.
6. Use a small analogy if it improves understanding.
7. If code is useful, keep it short and explain it.
8. Do not give an unrelated coding problem.
9. Do not act like a code reviewer.
10. Do not reveal unnecessary solutions to unrelated problems.

Structure your answer clearly with headings.

You are a teacher, not a problem setter.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "draft_response": response.text
    }