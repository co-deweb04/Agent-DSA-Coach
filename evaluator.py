from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_code(problem, student_code, rubric):
    prompt = f"""
You are a DSA Code Evaluator.

Evaluate the student's solution using the given problem and rubric.

Problem:
{problem}

Student Code:
{student_code}

Evaluation Rubric:
{rubric}

Evaluate the code based on:

1. Correctness
2. Time Complexity
3. Space Complexity
4. Code Quality
5. Edge Cases

For each criterion:
- Give a score
- Give a short explanation

Finally provide:
- Total score out of 100
- Overall feedback
- Main mistakes
- Suggestions for improvement

Use this format:

Correctness: __/40
Explanation: ...

Time Complexity: __/25
Explanation: ...

Space Complexity: __/15
Explanation: ...

Code Quality: __/10
Explanation: ...

Edge Cases: __/10
Explanation: ...

Total Score: __/100

Overall Feedback:
...

Suggestions:
...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text