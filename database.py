import psycopg2
from pgvector.psycopg2 import register_vector

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT
)


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


def initialize_database():

    conn = get_connection()

    try:
        with conn.cursor() as cur:

            # Enable pgvector
            cur.execute(
                "CREATE EXTENSION IF NOT EXISTS vector;"
            )

            # RAG knowledge table
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

            # Search history table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(100),
                    question TEXT NOT NULL,
                    mode VARCHAR(50),
                    response TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

        conn.commit()

    finally:
        conn.close()


def save_search_history(
    question,
    mode,
    response,
    user_id="default_user"
):
    """
    Save a student's question and the coach's response.
    """

    conn = get_connection()

    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO search_history
                (user_id, question, mode, response)
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


def get_search_history(
    user_id="default_user",
    limit=20
):
    """
    Get the student's previous searches.
    """

    conn = get_connection()

    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT question, mode, response, created_at
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