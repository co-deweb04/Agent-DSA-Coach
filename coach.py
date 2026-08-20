# coach.py

from graph import run_agent


def get_response(
    question,
    mode="learn",
    topic=None,
    difficulty=None,
    user_id=None,
    student_code=None,
    conversation_history=None
):

    state = {
        "question": question,
        "mode": mode,
        "topic": topic,
        "difficulty": difficulty,
        "user_id": user_id,
        "student_code": student_code,
        "history": conversation_history or [],
        "loop_count": 0,
    }

    result = run_agent(state)

    return result.get(
        "final_response",
        "Unable to generate a response."
    )