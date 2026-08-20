import psycopg2
from pgvector.psycopg2 import register_vector

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT
)


# =====================================
# DATABASE CONNECTION
# =====================================

def get_connection():

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    register_vector(conn)

    return conn


# =====================================
# INITIALIZE DATABASE
# =====================================

def initialize_database():

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            # Enable pgvector

            cur.execute(
                "CREATE EXTENSION IF NOT EXISTS vector;"
            )


            # RAG knowledge / embeddings

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB,
                    embedding VECTOR(384)
                );
                """
            )


            # Search / conversation history

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    question TEXT NOT NULL,
                    mode VARCHAR(50),
                    response TEXT,
                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


            # Conversations

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


            # Conversation messages

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,

                    conversation_id INTEGER
                        REFERENCES conversations(id)
                        ON DELETE CASCADE,

                    role VARCHAR(20) NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


            # Student uploaded code

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS student_code (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    filename TEXT NOT NULL,
                    file_type VARCHAR(20),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


        conn.commit()

    finally:

        conn.close()


# =====================================
# SEARCH HISTORY
# =====================================

def save_search_history(
    question,
    mode,
    response,
    user_id="default_user"
):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO search_history
                (
                    user_id,
                    question,
                    mode,
                    response
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    question,
                    mode,
                    response
                )
            )

        conn.commit()

    finally:

        conn.close()


# =====================================
# GET SEARCH HISTORY
# =====================================

def get_search_history(
    user_id="default_user",
    limit=20
):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    question,
                    mode,
                    response,
                    created_at
                FROM search_history
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (
                    user_id,
                    limit
                )
            )

            return cur.fetchall()

    finally:

        conn.close()


# =====================================
# CREATE CONVERSATION
# =====================================

def create_conversation(title):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO conversations (title)
                VALUES (%s)
                RETURNING id
                """,
                (title,)
            )

            conversation_id = cur.fetchone()[0]

        conn.commit()

        return conversation_id

    finally:

        conn.close()


# =====================================
# GET ALL CONVERSATIONS
# =====================================

def get_conversations():

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    id,
                    title
                FROM conversations
                ORDER BY created_at DESC
                """
            )

            return cur.fetchall()

    finally:

        conn.close()


# =====================================
# SAVE MESSAGE
# =====================================

def save_message(
    conversation_id,
    role,
    content
):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO messages
                (
                    conversation_id,
                    role,
                    content
                )
                VALUES (%s, %s, %s)
                """,
                (
                    conversation_id,
                    role,
                    content
                )
            )

        conn.commit()

    finally:

        conn.close()


# =====================================
# GET MESSAGES
# =====================================

def get_messages(conversation_id):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    role,
                    content
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC
                """,
                (conversation_id,)
            )

            return cur.fetchall()

    finally:

        conn.close()


# =====================================
# SAVE STUDENT CODE
# =====================================

def save_student_code(
    filename,
    file_type,
    content,
    user_id="default_user"
):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO student_code
                (
                    user_id,
                    filename,
                    file_type,
                    content
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    filename,
                    file_type,
                    content
                )
            )

        conn.commit()

    finally:

        conn.close()