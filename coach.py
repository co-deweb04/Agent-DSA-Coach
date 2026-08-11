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
# Convert Streamlit option to RAG mode
# ------------------------------------------------------------

def get_rag_mode(mode):

    mode_map = {
        "Learn DSA": "learn",
        "Practice": "practice",
        "Get Hint": "hint",
        "View Solution": "solution",
        "Code Review": "code_review"
    }

    return mode_map.get(mode, "general")


# ------------------------------------------------------------
# DSA Coach response
# ------------------------------------------------------------

def get_response(question, mode, uploaded_code=None):

    # --------------------------------------------------------
    # Convert UI mode to RAG mode
    # --------------------------------------------------------

    rag_mode = get_rag_mode(mode)


    # --------------------------------------------------------
    # Retrieve relevant knowledge from RAG
    # --------------------------------------------------------

    rag_result = retrieve_context(
        question=question,
        mode=rag_mode,
        include_code=bool(uploaded_code)
    )

    context = rag_result.get("context", "")


    # --------------------------------------------------------
    # Add uploaded code if available
    # --------------------------------------------------------

    code_section = ""

    if uploaded_code:

        code_section = f"""
## Student's uploaded code:

{uploaded_code}
"""


    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = f"""
You are a DSA Coach Agent.

Your job is to help students learn and practice
Data Structures and Algorithms.

Mode: {mode}

Relevant knowledge retrieved from the RAG system:
{context}

Student question:
{question}

{code_section}

Instructions:

- Explain concepts in simple and beginner-friendly language.
- Use examples whenever useful.
- Give hints instead of the complete answer in Hint mode.
- Explain solutions step by step in Solution mode.
- In Practice mode, provide an appropriate DSA problem.
- In Code Review mode, review the student's uploaded code.
- Identify errors, inefficient logic, and possible improvements.
- Explain why the suggested improvements are useful.
- If code is provided, refer to the student's actual code.
- Use the provided RAG context when answering.
- Do not invent information that conflicts with the provided context.
- Keep explanations suitable for a student learning DSA.
- Be clear and concise.
"""


    # --------------------------------------------------------
    # Generate Gemini response
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Unable to generate a response: {e}"