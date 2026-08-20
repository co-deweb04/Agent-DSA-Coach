# agents/practice_agent.py

from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context


client = genai.Client(api_key=GEMINI_API_KEY)


def practice_agent(state):

    question = state.get("question", "")
    topic = state.get("topic")
    difficulty = state.get("difficulty")
    user_id = state.get("user_id")

    result = retrieve_context(
        question=question,
        mode="practice",
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=False,
        include_leetcode=True,
        include_stories=False,
    )

    context = result.get("context", "")

    prompt = f"""
You are the Practice Agent of a DSA Coach.

Your job is to give the student a DSA coding problem to solve.

Student request:
{question}

Relevant problems retrieved from the knowledge base:
{context}

Instructions:

1. Give ONE suitable DSA problem.
2. Prefer a problem relevant to the student's requested topic.
3. Mention difficulty if available.
4. Clearly explain the problem.
5. Include input/output examples when appropriate.
6. Include constraints when available.
7. Do NOT give the complete solution.
8. Do NOT give complete code.
9. Do NOT reveal the algorithm immediately.
10. End by asking the student to attempt the problem.

If the student explicitly asks for a solution, they should use the Solution option.

Format:

## Problem
...

## Example
...

## Constraints
...

## Your Task
...

Do not solve the problem.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "draft_response": response.text
    }