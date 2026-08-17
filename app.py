import json
import streamlit as st

from coach import get_response

from database import (
    get_connection,
    create_conversation,
    get_conversations,
    get_messages,
    save_message
)


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

    # -----------------------------
    # NEW CHAT
    # -----------------------------

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.conversation_id = None

        st.rerun()

    st.divider()

    # -----------------------------
    # MODE
    # -----------------------------

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

    # -----------------------------
    # CHAT HISTORY
    # -----------------------------

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

                # Select conversation
                st.session_state.conversation_id = (
                    conversation_id
                )

                # Load messages
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
    "Your AI-powered assistant for learning "
    "and practicing Data Structures and Algorithms."
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
# CHAT INPUT
# =====================================

prompt = st.chat_input(
    "Ask anything about DSA...",
    accept_file=True,
    file_type=["py", "ipynb"]
)


# =====================================
# WHEN USER SENDS A MESSAGE
# =====================================

if prompt:

    # ---------------------------------
    # GET QUESTION
    # ---------------------------------

    question = prompt.text.strip()


    # ---------------------------------
    # GET UPLOADED FILE
    # ---------------------------------

    student_code = None

    if prompt.files:

        uploaded_file = prompt.files[0]

        # Python file
        if uploaded_file.name.endswith(".py"):

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


    # ---------------------------------
    # MAKE SURE QUESTION EXISTS
    # ---------------------------------

    if not question:

        if student_code:

            question = (
                "Please review the uploaded code."
            )

        else:

            st.warning(
                "Please enter a question."
            )

            st.stop()


    # =================================
    # CREATE NEW CONVERSATION
    # =================================

    if st.session_state.conversation_id is None:

        # Use question as chat title
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
    # BUILD PREVIOUS CONVERSATION
    # =================================
    #
    # IMPORTANT:
    # Build this BEFORE adding the
    # current question.
    #
    # This prevents Gemini from
    # receiving the current question
    # twice.
    # =================================

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

        if prompt.files:

            st.caption(
                f"📎 {prompt.files[0].name}"
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
    # GET AI RESPONSE
    # =================================

    with st.chat_message("assistant"):

        with st.spinner(
            "DSA Coach is thinking..."
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

    # Refresh sidebar so the new
    # conversation appears immediately
    st.rerun()