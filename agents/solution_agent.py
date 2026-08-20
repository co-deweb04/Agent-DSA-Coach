# agents/solution_agent.py

from google import genai
from config import GEMINI_API_KEY
from rag import retrieve_context


client = genai.Client(api_key=GEMINI_API_KEY)


def solution_agent(state):

    question = state.get("question", "")
    topic = state.get("topic")
    difficulty = state.get("difficulty")
    user_id = state.get("user_id")

    result = retrieve_context(
        question=question,
        mode="solution",
        topic=topic,
        difficulty=difficulty,
        user_id=user_id,
        include_code=False,
        include_leetcode=True,
        include_stories=False,
    )

    context = result.get("context", "")

    prompt = f"""
You are the Solution Agent of a DSA Coach.

The student explicitly wants a solution.

Student request:
{question}

Relevant DSA/problem knowledge:
{context}

Instructions:

1. Identify the problem clearly.
2. Explain the approach before showing code.
3. Explain the algorithm step by step.
4. Provide a complete working solution.
5. Prefer Java unless the student explicitly requests another language.
6. Explain important parts of the code.
7. Give time complexity.
8. Give space complexity.
9. Mention important edge cases.
10. Make the answer suitable for coding interviews and LeetCode.

Use this structure:

## Approach

## Algorithm

## Code

## Explanation

## Complexity

## Edge Cases

Unlike the Practice and Hint agents, you ARE allowed to provide the complete solution.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "draft_response": response.text
    }