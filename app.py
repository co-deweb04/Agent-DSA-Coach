import json
import streamlit as st

from coach import get_response

from database import (
    initialize_database,
    create_conversation,
    get_conversations,
    get_messages,
    save_message,
    save_student_code
)


# =====================================
# DATABASE INITIALIZATION
# =====================================

initialize_database()


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="DSA Coach",
    page_icon="🧠",
    layout="wide"
)


# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🧠 DSA Coach")

    # New conversation

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.conversation_id = None

        st.rerun()

    st.divider()


    # Agent mode

    option = st.selectbox(
        "Choose an option",
        [
            "Learn DSA",
            "Practice",
            "Get Hint",
            "View Solution",
            "Code Review"
        ]
    )

    st.divider()


    # Conversation history

    st.subheader("💬 Chat History")

    conversations = get_conversations()

    if not conversations:

        st.caption("No previous chats yet.")

    else:

        for conversation_id, title in conversations:

            if st.button(
                title,
                key=f"chat_{conversation_id}",
                use_container_width=True
            ):

                st.session_state.conversation_id = (
                    conversation_id
                )

                db_messages = get_messages(
                    conversation_id
                )

                st.session_state.messages = [
                    {
                        "role": role,
                        "content": content
                    }
                    for role, content in db_messages
                ]

                st.rerun()


# =====================================
# MAIN TITLE
# =====================================

st.title("🧠 DSA Coach Agent")

st.caption(
    "Your AI-powered assistant for learning, "
    "practicing, debugging and reviewing "
    "Data Structures and Algorithms."
)


# =====================================
# AGENT ARCHITECTURE
# =====================================

st.info(
    "Powered by LangGraph Agent Orchestration, "
    "RAG, Gemini, Code Evaluation and "
    "a Critic-based verification loop."
)


# =====================================
# DISPLAY CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =====================================
# CHAT INPUT + FILE UPLOAD
# =====================================

prompt = st.chat_input(
    "Ask anything about DSA...",
    accept_file=True,
    file_type=["py", "ipynb"]
)


# =====================================
# PROCESS USER REQUEST
# =====================================

if prompt:

    # Get question

    question = prompt.text.strip()


    # =================================
    # PROCESS STUDENT CODE
    # =================================

    student_code = None
    uploaded_filename = None
    uploaded_file_type = None

    if prompt.files:

        uploaded_file = prompt.files[0]

        uploaded_filename = uploaded_file.name


        # Python file

        if uploaded_file.name.endswith(".py"):

            uploaded_file_type = "py"

            student_code = (
                uploaded_file
                .getvalue()
                .decode(
                    "utf-8",
                    errors="ignore"
                )
            )


        # Jupyter Notebook

        elif uploaded_file.name.endswith(".ipynb"):

            uploaded_file_type = "ipynb"

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

            student_code = "\n\n".join(
                code_parts
            )


        # Save uploaded code

        if student_code:

            save_student_code(
                filename=uploaded_filename,
                file_type=uploaded_file_type,
                content=student_code
            )


    # =================================
    # VALIDATE QUESTION
    # =================================

    if not question:

        if student_code:

            question = (
                "Please review the uploaded code "
                "and identify correctness, "
                "complexity, errors and improvements."
            )

        else:

            st.warning(
                "Please enter a question."
            )

            st.stop()


    # =================================
    # CREATE CONVERSATION
    # =================================

    if st.session_state.conversation_id is None:

        title = question.strip()

        if len(title) > 40:

            title = title[:40] + "..."

        conversation_id = create_conversation(
            title
        )

        st.session_state.conversation_id = (
            conversation_id
        )

    else:

        conversation_id = (
            st.session_state.conversation_id
        )


    # =================================
    # BUILD CONVERSATION HISTORY
    # =================================

    conversation_history = ""

    for message in st.session_state.messages:

        conversation_history += (
            message["role"].upper()
            + ": "
            + message["content"]
            + "\n\n"
        )


    # =================================
    # DISPLAY USER MESSAGE
    # =================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

        if uploaded_filename:

            st.caption(
                f"📎 {uploaded_filename}"
            )


    # =================================
    # SAVE USER MESSAGE
    # =================================

    save_message(
        conversation_id,
        "user",
        question
    )


    # =================================
    # LANGGRAPH AGENT EXECUTION
    # =================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 DSA Coach is thinking..."
        ):

            response = get_response(
                question=question,
                mode=option,
                conversation_history=(
                    conversation_history
                ),
                student_code=student_code
            )

        st.markdown(response)


    # =================================
    # SAVE AI RESPONSE
    # =================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    save_message(
        conversation_id,
        "assistant",
        response
    )


    # =================================
    # REFRESH APPLICATION
    # =================================

    st.rerun()