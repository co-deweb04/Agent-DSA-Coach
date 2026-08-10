import streamlit as st
from coach import get_response

st.set_page_config(
    page_title="DSA Coach",
    page_icon="🧠"
)

st.title("🧠 DSA Coach Agent")

st.write(
    "Your AI-powered assistant for learning and practicing "
    "Data Structures and Algorithms."
)

# Sidebar
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

# Question
question = st.text_area(
    "Enter your DSA question:"
)

# File upload
uploaded_file = st.file_uploader(
    "Upload your Python file",
    type=["py", "ipynb"]
)

if st.button("Ask Coach"):

    if question:
        response = get_response(question, option)
        st.write(response)

    elif uploaded_file:
        st.write("File uploaded successfully!")

    else:
        st.warning("Please enter a question or upload a file.")