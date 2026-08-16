from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_rubric(problem, difficulty):
    prompt = f"""
Create an evaluation rubric for this DSA problem.

Problem:
{problem}

Difficulty:
{difficulty}

Include these criteria:
- Correctness
- Time complexity
- Space complexity
- Code quality
- Edge cases

Assign appropriate weights so that the total is 100%.

Return the rubric in this format:

Correctness: XX%
Time Complexity: XX%
Space Complexity: XX%
Code Quality: XX%
Edge Cases: XX%

Then briefly explain what should be checked for each criterion.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text