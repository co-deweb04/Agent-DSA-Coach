# agents/hint_agent.py

from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context


client = genai.Client(api_key=GEMINI_API_KEY)


def hint_agent(state):

    question = state.get("question", "")
    topic = state.get("topic")
    difficulty = state.get("difficulty")
    user_id = state.get("user_id")
    student_code = state.get("student_code")

    # Include the student's code when available
    retrieval_question = question

    if student_code:
        retrieval_question += "\n\nStudent's code:\n" + student_code

    result = retrieve_context(
        question=retrieval_question,
        mode="hint",
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=bool(student_code),
        include_leetcode=True,
        include_stories=False,
    )

    context = result.get("context", "")

    prompt = f"""
You are the Hint Agent of a DSA Coach.

Your job is to help a student who is stuck WITHOUT giving away the solution.

Student question:
{question}

Student code, if provided:
{student_code or "No code provided."}

Relevant knowledge:
{context}

Instructions:

1. Give a small and useful hint.
2. Focus on the student's current difficulty.
3. Do not provide the complete solution.
4. Do not provide complete code.
5. Do not directly reveal the final algorithm.
6. Ask the student to think about the next step.
7. If the student is still stuck, a stronger hint can be given later.
8. Keep the hint focused on the current problem.

Your response should feel like a mentor helping the student discover the answer.

Start with:

### Hint

Then provide the hint.

Do not provide a solution.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "draft_response": response.text
    }