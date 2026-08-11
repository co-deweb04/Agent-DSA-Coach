import psycopg2
from pgvector.psycopg2 import register_vector

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    EMBEDDING_DIMENSION
)


def get_connection():
    """Create a PostgreSQL connection."""

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
    """Create the pgvector extension and RAG table."""

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    try:
        cursor = conn.cursor()

        # Enable pgvector
        cursor.execute(
            "CREATE EXTENSION IF NOT EXISTS vector;"
        )

        # Create table expected by rag.py
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS rag_chunks (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                metadata JSONB,
                embedding VECTOR({EMBEDDING_DIMENSION})
            );
            """
        )

        # Cosine similarity index
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS rag_chunks_embedding_idx
            ON rag_chunks
            USING hnsw (embedding vector_cosine_ops);
            """
        )

        conn.commit()

        print("PostgreSQL + pgvector initialized successfully.")
        print("rag_chunks table is ready.")

    except Exception as e:
        conn.rollback()
        print("Database initialization failed:")
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    initialize_database()