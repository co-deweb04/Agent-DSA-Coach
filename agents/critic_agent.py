# This is the important part for reasoning/verification loop

from google import genai
from config import GEMINI_API_KEY, MAX_REASONING_LOOPS

client = genai.Client(api_key=GEMINI_API_KEY)


def critic_agent(state):

    draft = state.get("draft_response", "")
    question = state.get("question", "")
    loop_count = state.get("loop_count", 0)

    prompt = f"""
You are a Critic Agent for a DSA Coach.

Evaluate the draft answer.

Student question:
{question}

Draft:
{draft}

Check:

1. Is the answer technically correct?
2. Does it answer the question?
3. Are time and space complexities correct?
4. Is the explanation clear?
5. Does it contain unsupported or contradictory information?

Return exactly:

PASS
or
RETRY: <short reason>
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    critique = response.text.strip()

    retry = critique.upper().startswith("RETRY")

    if loop_count >= MAX_REASONING_LOOPS:
        retry = False

    return {
        "critique": critique,
        "needs_retry": retry,
        "loop_count": loop_count + 1
    }