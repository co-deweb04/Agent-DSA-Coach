
import json
import streamlit as st

from coach import get_response


# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="DSA Coach",
    page_icon="🧠"
)


# ------------------------------------------------------------
# Title
# ------------------------------------------------------------

st.title("🧠 DSA Coach Agent")

st.write(
    "Your AI-powered assistant for learning and practicing "
    "Data Structures and Algorithms."
)


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.title("DSA Coach")

option = st.sidebar.selectbox(
    "Choose an option",
    [
        "Learn DSA",
        "Practice",
        "Get Hint",
        "View Solution",
        "Code Review"
    ]
)


# ------------------------------------------------------------
# Question
# ------------------------------------------------------------

question = st.text_area(
    "Enter your DSA question:"
)


# ------------------------------------------------------------
# File upload
# ------------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your Python file",
    type=["py", "ipynb"]
)


# ------------------------------------------------------------
# Read uploaded file
# ------------------------------------------------------------

uploaded_code = None

if uploaded_file:

    file_name = uploaded_file.name

    if file_name.endswith(".py"):

        uploaded_code = uploaded_file.read().decode("utf-8")

    elif file_name.endswith(".ipynb"):

        notebook = json.load(uploaded_file)

        code_cells = []

        for cell in notebook.get("cells", []):

            if cell.get("cell_type") == "code":

                source = "".join(cell.get("source", []))
                code_cells.append(source)

        uploaded_code = "\n\n".join(code_cells)

    st.success(f"Uploaded: {file_name}")


# ------------------------------------------------------------
# Ask Coach
# ------------------------------------------------------------

if st.button("Ask Coach"):

    if not question and not uploaded_code:

        st.warning(
            "Please enter a question or upload a file."
        )

    else:

        # If only a file is uploaded, create a suitable question
        if not question:
            question = "Please review my uploaded code."

        response = get_response(
            question,
            option,
            uploaded_code
        )

        st.write(response)

