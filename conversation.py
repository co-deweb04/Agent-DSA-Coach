from database import get_connection

#Conversation management functions
def create_conversation(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (title)
        VALUES (%s)
        RETURNING id
        """,
        (title,)
    )

    conversation_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return conversation_id

#Saving messages to the database
def save_message(conversation_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (conversation_id, role, content)
        VALUES (%s, %s, %s)
        """,
        (conversation_id, role, content)
    )

    conn.commit()
    cursor.close()
    conn.close()

def get_messages(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return messages
#get all conversations
def get_conversations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title
        FROM conversations
        ORDER BY updated_at DESC
        """
    )

    conversations = cursor.fetchall()

    cursor.close()
    conn.close()

    return conversations