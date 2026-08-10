# DSA Coach Agent

An AI-powered DSA learning assistant that helps students understand Data Structures and Algorithms through explanations, hints, code review, practice questions, and personalized feedback.

## Features

- DSA concept explanations
- Story-based explanations for difficult concepts
- Hints without directly revealing the solution
- Solution explanations
- Python code review
- `.py` file upload
- `.ipynb` file upload
- RAG-based contextual responses
- 45 LeetCode practice questions
  - 15 Easy
  - 15 Medium
  - 15 Hard
- Student attempt tracking
- Progress tracking
- PostgreSQL database with pgvector

## Project Architecture

DSA-Coach-Agent/
│
├── .gitignore
├── .env
├── README.md
├── requirements.txt
│
├── app.py
├── coach.py
├── rag.py
├── ingest.py
├── database.py
├── config.py
├── create_tables.sql
│
├── data/
│   ├── notes/
│   ├── stories/
│   ├── descriptions/
│   └── leetcode.json
│
└── uploads/

## Architecture Flow

Student
   ↓
Streamlit (app.py)
   ↓
DSA Coach (coach.py)
   ↓
RAG (rag.py)
   ↓
Relevant DSA Context
   ↓
LLM
   ↓
Explanation / Hint / Code Feedback
   ↓
PostgreSQL

## File Responsibilities

### app.py
Streamlit user interface.

### coach.py
Main DSA Coach logic and LLM interaction.

### rag.py
Retrieval-Augmented Generation and relevant context retrieval.

### ingest.py
Processes DSA learning material and creates chunks/embeddings.

### database.py
Handles PostgreSQL database operations.

### config.py
Application and environment configuration.

### create_tables.sql
SQL commands for creating the required database tables.

## Team Responsibilities

### Member 1 — Data & RAG
- DSA notes
- Stories
- Descriptions
- LeetCode dataset
- Data ingestion
- Chunking
- Embeddings
- RAG retrieval

### Member 2 — Database & Storage
- PostgreSQL
- pgvector
- Database schema
- File storage
- `.py` and `.ipynb` handling
- Student attempts
- Progress tracking

### Member 3 — DSA Coach & UI
- DSA Coach agent
- LLM prompts
- Explanations
- Hints
- Code review
- Streamlit interface
- Integration of RAG and database

## Technologies Used

- Python
- Streamlit
- PostgreSQL
- pgvector
- LLM
- RAG
- Embeddings
- Git & GitHub

## Setup

### 1. Clone the repository

git clone <repository-url>

cd DSA-Coach-Agent

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the environment

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Configure environment variables

Create a `.env` file and add the required API keys
and PostgreSQL configuration.

### 6. Set up PostgreSQL

Create the database and run:

create_tables.sql

### 7. Run the application

streamlit run app.py

## Git Workflow

Each member works on their own branch:

member1-rag
member2-database
member3-coach-ui

After completing and testing the work, the branch can be merged
into the main branch.

## Future Improvements

- Personalized learning paths
- Difficulty prediction
- More DSA problems
- Performance analytics
- Voice-based interaction
- More programming language support