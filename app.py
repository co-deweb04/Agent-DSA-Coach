import json
import streamlit as st

from coach import get_response


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="DSA Coach",
    page_icon="🧠"
)


# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "chat_started" not in st.session_state:
    st.session_state.chat_started = False


# =====================================
# TITLE
# =====================================

st.title("🧠 DSA Coach Agent")

st.write(
    "Your AI-powered assistant for learning "
    "and practicing Data Structures and Algorithms."
)


# =====================================
# SIDEBAR
# =====================================

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


# =====================================
# DISPLAY OLD MESSAGES
# =====================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# =====================================
# FILE UPLOAD
# =====================================

uploaded_file = None

if option == "Code Review":

    uploaded_file = st.file_uploader(
        "Upload your Python file",
        type=["py", "ipynb"]
    )


# =====================================
# INITIAL QUESTION
# =====================================

if not st.session_state.chat_started:

    question = st.text_area(
        "Ask your DSA question:",
        placeholder="Example: Explain binary search"
    )

    if st.button("Ask Coach"):

        if not question:

            st.warning(
                "Please enter a question."
            )

        else:

            student_code = None

            # Read uploaded Python file
            if uploaded_file:

                if uploaded_file.name.endswith(".py"):

                    student_code = (
                        uploaded_file
                        .getvalue()
                        .decode(
                            "utf-8",
                            errors="ignore"
                        )
                    )

                # Read Jupyter Notebook
                elif uploaded_file.name.endswith(".ipynb"):

                    notebook = json.loads(
                        uploaded_file
                        .getvalue()
                        .decode(
                            "utf-8",
                            errors="ignore"
                        )
                    )

                    code_parts = []

                    for cell in notebook.get(
                        "cells",
                        []
                    ):

                        if cell.get(
                            "cell_type"
                        ) == "code":

                            source = cell.get(
                                "source",
                                []
                            )

                            code_parts.append(
                                "".join(source)
                            )

                    student_code = (
                        "\n\n".join(
                            code_parts
                        )
                    )

            # Store user message
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.spinner(
                "DSA Coach is thinking..."
            ):

                response = get_response(
                    question,
                    option,
                    student_code=student_code
                )

            # Store assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.session_state.chat_started = True

            st.rerun()


# =====================================
# FOLLOW-UP QUESTION
# =====================================

else:

    st.subheader(
        "💬 Ask a follow-up question"
    )

    follow_up = st.text_area(
        "Continue the conversation:",
        placeholder=(
            "Example: Why is the time "
            "complexity O(log n)?"
        ),
        key="follow_up_question"
    )

    if st.button("Ask Follow-up"):

        if not follow_up:

            st.warning(
                "Please enter a follow-up question."
            )

        else:

            # Build conversation history
            conversation_history = ""

            for message in (
                st.session_state.messages
            ):

                conversation_history += (
                    message["role"].upper()
                    + ": "
                    + message["content"]
                    + "\n\n"
                )

            # Store user message
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": follow_up
                }
            )

            with st.spinner(
                "DSA Coach is thinking..."
            ):

                response = get_response(
                    follow_up,
                    option,
                    conversation_history
                )

            # Store response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.rerun()


# =====================================
# NEW CHAT
# =====================================

if st.session_state.chat_started:

    if st.sidebar.button("🗑️ New Chat"):

        st.session_state.messages = []

        st.session_state.chat_started = False

        st.rerun()