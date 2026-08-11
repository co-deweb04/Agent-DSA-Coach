# DSA Coach Agent

An AI-powered DSA learning assistant that helps students understand **Data Structures and Algorithms** through explanations, hints, code review, practice questions, and personalized feedback.

## Features

* DSA concept explanations
* Story-based explanations for difficult concepts
* Hints without directly revealing the solution
* Step-by-step solution explanations
* Python code review
* `.py` file upload
* `.ipynb` file upload
* RAG-based contextual responses
* 45 LeetCode practice questions

  * 15 Easy
  * 15 Medium
  * 15 Hard
* Student attempt tracking
* Progress tracking
* PostgreSQL database with pgvector
* Semantic search using BGE embeddings
* Gemini-powered responses

## Project Architecture

```text
DSA-Coach-Agent/
│
├── .gitignore
├── key.env
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
```

> **Security:** `key.env` contains API keys and database credentials and must not be committed to GitHub.

## Architecture Flow

```text
Student
   ↓
Streamlit (app.py)
   ↓
DSA Coach (coach.py)
   ↓
RAG (rag.py)
   ↓
Intent Detection
   ↓
Query Embedding
   ↓
PostgreSQL + pgvector
   ↓
Similarity Search
   ↓
Filtering + Deduplication
   ↓
Reranking
   ↓
Relevant DSA Context
   ↓
Gemini 2.5 Flash
   ↓
Explanation / Hint / Solution / Code Feedback
   ↓
Streamlit UI
```

## File Responsibilities

### `app.py`

Provides the Streamlit user interface.

Responsibilities:

* DSA learning interface
* Practice mode
* Hint mode
* Solution mode
* Code review mode
* `.py` file upload
* `.ipynb` file upload
* Displays the final response

### `coach.py`

Main DSA Coach logic and Gemini LLM interaction.

Responsibilities:

* Receives the student's question
* Converts the selected UI option into a RAG mode
* Calls the RAG system
* Builds the LLM prompt
* Includes uploaded student code
* Sends the prompt to Gemini
* Returns the final response

### `rag.py`

Retrieval-Augmented Generation retrieval layer.

Responsibilities:

* Intent detection
* Query embedding
* PostgreSQL + pgvector search
* Similarity filtering
* Deduplication
* Reranking
* Category-balanced context selection
* Context formatting
* Source tracking

The RAG layer does **not** generate the final answer. It provides relevant information to `coach.py`.

### `ingest.py`

Processes DSA learning material and stores embeddings in PostgreSQL.

Responsibilities:

* Load Markdown DSA notes
* Split documents into chunks
* Generate embeddings
* Store chunks and embeddings in PostgreSQL

### `database.py`

Handles PostgreSQL and pgvector operations.

Responsibilities:

* PostgreSQL connection
* pgvector registration
* Enable the `vector` extension
* Create the `rag_chunks` table
* Create the vector similarity index

### `config.py`

Stores application configuration.

It contains:

* Gemini API configuration
* PostgreSQL configuration
* Embedding model
* Embedding dimension
* RAG configuration

### `create_tables.sql`

Contains SQL commands for creating the required database tables.

## RAG Configuration

The project uses:

```text
Embedding Model:
BAAI/bge-small-en-v1.5

Embedding Dimension:
384

Vector Database:
PostgreSQL + pgvector

Similarity:
Cosine similarity
```

The same embedding model and dimension must be used when ingesting documents and retrieving information.

## Team Responsibilities

### Member 1 — Data & RAG

* DSA notes
* Stories
* Descriptions
* LeetCode dataset
* Data ingestion
* Chunking
* Embeddings
* RAG retrieval
* Similarity search

### Member 2 — Database & Storage

* PostgreSQL
* pgvector
* Database schema
* File storage
* `.py` and `.ipynb` handling
* Student attempts
* Progress tracking

### Member 3 — DSA Coach & UI

* DSA Coach agent
* Gemini LLM integration
* LLM prompts
* Explanations
* Hints
* Solution explanations
* Code review
* Streamlit interface
* Integration of RAG and database

## Technologies Used

* Python
* Streamlit
* PostgreSQL
* pgvector
* Gemini 2.5 Flash
* LangChain
* Hugging Face Sentence Transformers
* RAG
* Embeddings
* Git & GitHub

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd DSA-Coach-Agent
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a file named:

```text
key.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key

DB_NAME=dsa_coach
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit `key.env` to GitHub.

### 6. Set up PostgreSQL

Create the PostgreSQL database:

```text
dsa_coach
```

Make sure the **pgvector** extension is installed.

The application can create the extension and `rag_chunks` table through:

```bash
python database.py
```

### 7. Add DSA learning material

Place Markdown files inside:

```text
data/notes/
```

For example:

```text
data/notes/
├── arrays.md
├── stacks.md
├── queues.md
├── linked_lists.md
└── binary_search.md
```

### 8. Run RAG ingestion

Run:

```bash
python ingest.py
```

This will:

1. Load the Markdown files.
2. Split them into chunks.
3. Generate BGE embeddings.
4. Store the chunks and embeddings in PostgreSQL.

### 9. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Git Workflow

Each team member works on their own branch:

```text
member1-rag
member2-database
member3-coach-ui
```

After completing and testing the work:

```text
Member Branch
     ↓
Commit
     ↓
Push
     ↓
Pull Request
     ↓
Review
     ↓
Merge into main
```

## Security

* API keys are stored in `key.env`.
* Database passwords are stored in `key.env`.
* `key.env` must be included in `.gitignore`.
* Database queries use parameterized SQL.
* Student code retrieval requires a `user_id`.
* Student code should not be exposed to other users.

## Future Improvements

* Personalized learning paths
* Difficulty prediction
* More DSA problems
* Performance analytics
* Voice-based interaction
* More programming language support
* Adaptive question recommendations
* Detailed student progress dashboards
