-- =====================================
-- PGVECTOR EXTENSION
-- =====================================

CREATE EXTENSION IF NOT EXISTS vector;


-- =====================================
-- RAG KNOWLEDGE / EMBEDDINGS
-- =====================================

CREATE TABLE IF NOT EXISTS rag_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(384)
);


-- =====================================
-- STUDENT SEARCH / CONVERSATION HISTORY
-- =====================================

CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    question TEXT NOT NULL,
    mode VARCHAR(50),
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- CONVERSATIONS
-- =====================================

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- CONVERSATION MESSAGES
-- =====================================

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER
        REFERENCES conversations(id)
        ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- STUDENT UPLOADED CODE
-- =====================================

CREATE TABLE IF NOT EXISTS student_code (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    filename TEXT NOT NULL,
    file_type VARCHAR(20),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);