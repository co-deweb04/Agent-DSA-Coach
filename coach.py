from google import genai

from config import GEMINI_API_KEY
from rag import retrieve_context
from database import save_search_history

from rubric_generator import generate_rubric
from evaluator import evaluate_code


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def get_response(
    question,
    mode,
    conversation_history="",
    student_code=None,
    user_id="default_user"
):
    """
    Main DSA Coach function.

    question:
        Current student question.

    mode:
        Learn DSA, Practice, Get Hint,
        View Solution or Code Review.

    conversation_history:
        Previous conversation in the current chat.

    student_code:
        Uploaded .py or .ipynb code.

    user_id:
        Student identifier.
    """

    # =====================================
    # CODE REVIEW
    # =====================================

    if mode == "Code Review":

        if not student_code:

            return (
                "Please upload a .py or .ipynb "
                "file for code review."
            )

        context = retrieve_context(question)

        rubric = generate_rubric(
            question,
            "General"
        )

        result = evaluate_code(
            question,
            student_code,
            rubric
        )

        response = f"""
## 🧠 DSA Code Review

### Relevant DSA Knowledge

{context}

### Evaluation Rubric

{rubric}

### Code Evaluation

{result}
"""

        save_search_history(
            question,
            mode,
            response,
            user_id
        )

        return response

    # =====================================
    # NORMAL DSA QUESTIONS
    # =====================================

    context = retrieve_context(question)

    prompt = f"""
You are an AI DSA Coach.

Your goal is to help students learn
Data Structures and Algorithms.

Current mode:
{mode}

Relevant knowledge retrieved from the
DSA knowledge base:

{context}


Previous conversation:

{conversation_history}


Current student question:

{question}


Instructions:

- Explain concepts in simple language.
- Use examples when useful.
- In Learn DSA mode, teach step by step.
- In Practice mode, guide the student
  without immediately revealing the answer.
- In Get Hint mode, provide hints only.
- In View Solution mode, explain the
  solution step by step.
- Maintain the context of the previous
  conversation.
- Answer the current question directly.
- Use the retrieved knowledge when relevant.
- Do not invent information that conflicts
  with the retrieved context.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    answer = response.text

    # Save question and answer
    save_search_history(
        question,
        mode,
        answer,
        user_id
    )

    return answer