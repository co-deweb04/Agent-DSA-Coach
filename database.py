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
# SEARCH HISTORY
# =====================================

def save_search_history(
    question,
    mode,
    response,
    user_id="default_user"
):
    """
    Save a student's question and response.
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
    Get previous searches.
    """

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT question,
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
# CONVERSATIONS
# =====================================

def create_conversation(title):
    """
    Create a new conversation
    and return its ID.
    """

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
    """
    Get all previous conversations
    for the sidebar.
    """

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT id, title
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
    """
    Save a user or assistant message.
    """

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO messages
                (conversation_id, role, content)
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
    """
    Get all messages belonging
    to one conversation.
    """

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT role, content
                FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC
                """,
                (conversation_id,)
            )

            return cur.fetchall()

    finally:

        conn.close()