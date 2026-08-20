# agents/router.py
# ============================================================
# Routes the request to the correct specialized agent.
# Sidebar mode has priority over automatic detection.
# ============================================================


def route_intent(state):

    question = str(state.get("question", "")).lower().strip()
    mode = str(state.get("mode", "")).lower().strip()

    # --------------------------------------------------------
    # Sidebar mode has highest priority
    # --------------------------------------------------------

    mode_mapping = {
        "learn": "learn",
        "learn dsa": "learn",

        "practice": "practice",

        "hint": "hint",
        "get hint": "hint",

        "solution": "solution",
        "view solution": "solution",

        "code_review": "code_review",
        "code review": "code_review",
    }

    if mode in mode_mapping:
        return {
            "intent": mode_mapping[mode]
        }

    # --------------------------------------------------------
    # Automatic detection
    # Used when no valid sidebar mode is supplied.
    # --------------------------------------------------------

    if any(word in question for word in [
        "review",
        "debug",
        "error",
        "wrong answer",
        "bug",
        "optimize",
        "optimization",
        "runtime error",
        "tle",
    ]):
        return {
            "intent": "code_review"
        }

    if any(word in question for word in [
        "hint",
        "clue",
        "stuck",
        "nudge",
    ]):
        return {
            "intent": "hint"
        }

    if any(word in question for word in [
        "solution",
        "solve",
        "answer",
        "complete code",
    ]):
        return {
            "intent": "solution"
        }

    if any(word in question for word in [
        "practice",
        "leetcode",
        "coding problem",
        "practice problem",
    ]):
        return {
            "intent": "practice"
        }

    # Default
    return {
        "intent": "learn"
    }