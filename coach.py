from google import genai

from config import GEMINI_API_KEY
from rag import retrieve_context


# ------------------------------------------------------------
# Gemini client
# ------------------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ------------------------------------------------------------
# Convert UI option to RAG mode
# ------------------------------------------------------------

def get_mode(option):

    mode_map = {
        "Learn DSA": "learn",
        "Practice": "practice",
        "Get Hint": "hint",
        "View Solution": "solution",
        "Code Review": "code_review"
    }

    return mode_map.get(option, "general")


# ------------------------------------------------------------
# DSA Coach response
# ------------------------------------------------------------

def get_response(question, mode, uploaded_code=None):

    # --------------------------------------------------------
    # Convert Streamlit option to RAG mode
    # --------------------------------------------------------

    rag_mode = get_mode(mode)

    # --------------------------------------------------------
    # Retrieve relevant knowledge from RAG
    # --------------------------------------------------------

    rag_result = retrieve_context(
        question=question,
        mode=rag_mode,
        include_code=uploaded_code is not None
    )

    context = rag_result.get("context", "")

    # --------------------------------------------------------
    # Add uploaded code if available
    # --------------------------------------------------------

    code_section = ""

    if uploaded_code:

        code_section = f"""
Student's uploaded code:

{uploaded_code}
"""