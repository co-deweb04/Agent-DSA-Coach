# graph.py

from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.router import route_intent
from agents.learning_agent import learning_agent
from agents.practice_agent import practice_agent
from agents.hint_agent import hint_agent
from agents.solution_agent import solution_agent
from agents.code_review_agent import code_review_agent
from agents.critic_agent import critic_agent


def choose_agent(state):

    intent = state.get("intent", "learn")

    if intent == "practice":
        return "practice"

    if intent == "hint":
        return "hint"

    if intent == "solution":
        return "solution"

    if intent in ["code_review", "debug"]:
        return "code_review"

    return "learn"


def check_critic(state):

    if state.get("needs_retry", False):
        return "retry"

    return "finish"


def prepare_retry(state):

    critique = state.get("critique", "")

    return {
        "question": (
            state.get("question", "")
            + "\n\nImprove the previous answer based on this critique:\n"
            + critique
        ),
        "loop_count": state.get("loop_count", 0) + 1,
    }


def final_response(state):

    return {
        "final_response": state.get(
            "draft_response",
            "Unable to generate a response."
        )
    }


def build_graph():

    graph = StateGraph(AgentState)

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    graph.add_node("router", route_intent)

    graph.add_node("learn", learning_agent)
    graph.add_node("practice", practice_agent)
    graph.add_node("hint", hint_agent)
    graph.add_node("solution", solution_agent)
    graph.add_node("code_review", code_review_agent)

    graph.add_node("critic", critic_agent)

    graph.add_node("retry", prepare_retry)
    graph.add_node("final", final_response)

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

    graph.add_edge(START, "router")

    # --------------------------------------------------------
    # Router → Agent
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "router",
        choose_agent,
        {
            "learn": "learn",
            "practice": "practice",
            "hint": "hint",
            "solution": "solution",
            "code_review": "code_review",
        }
    )

    # --------------------------------------------------------
    # Agent → Critic
    # --------------------------------------------------------

    graph.add_edge("learn", "critic")
    graph.add_edge("practice", "critic")
    graph.add_edge("hint", "critic")
    graph.add_edge("solution", "critic")
    graph.add_edge("code_review", "critic")

    # --------------------------------------------------------
    # Critic → Retry / Final
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "critic",
        check_critic,
        {
            "retry": "retry",
            "finish": "final",
        }
    )

    # --------------------------------------------------------
    # Retry → Router
    # --------------------------------------------------------

    graph.add_edge("retry", "router")

    # --------------------------------------------------------
    # Final → End
    # --------------------------------------------------------

    graph.add_edge("final", END)

    return graph.compile()


# Create compiled graph
dsa_graph = build_graph()


# ------------------------------------------------------------
# Public function used by coach.py
# ------------------------------------------------------------

def run_agent(initial_state):

    result = dsa_graph.invoke(initial_state)

    return result