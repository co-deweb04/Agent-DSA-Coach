# ============================================================
# rag.py
# ============================================================
#
# RAG Retrieval Layer for DSA Coach Agent
#
# Responsibilities:
#
# 1. Load the embedding model
# 2. Connect to PostgreSQL
# 3. Convert user query into an embedding
# 4. Perform semantic search using pgvector
# 5. Apply metadata filters
# 6. Retrieve DSA knowledge
# 7. Retrieve LeetCode questions
# 8. Retrieve student Python / Notebook code
# 9. Build context for the LLM
#
# ============================================================


import json
import psycopg2

from langchain_huggingface import HuggingFaceEmbeddings


# ============================================================
# CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# PostgreSQL configuration
# ------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "database": "dsa_coach",
    "user": "postgres",
    "password": "YOUR_PASSWORD",
    "port": 5432
}


# ------------------------------------------------------------
# Embedding model
# ------------------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ------------------------------------------------------------
# Number of documents to retrieve
# ------------------------------------------------------------

DEFAULT_K = 5


# ============================================================
# DSA RAG CLASS
# ============================================================

class DSA_RAG:
    """
    Retrieval-Augmented Generation retrieval layer
    for the DSA Coach Agent.

    This class retrieves relevant information from
    PostgreSQL + pgvector.

    It can retrieve:

    - DSA notes
    - DSA stories
    - DSA descriptions
    - LeetCode questions
    - Student .py files
    - Student .ipynb files
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        db_config=DB_CONFIG
    ):

        # ----------------------------------------------------
        # Store database configuration
        # ----------------------------------------------------

        self.db_config = db_config

        # ----------------------------------------------------
        # Load embedding model
        # ----------------------------------------------------

        print("Loading embedding model...")

        self.embedder = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,

            encode_kwargs={
                # Normalize vectors for cosine similarity
                "normalize_embeddings": True
            }
        )

        print("Embedding model loaded successfully.")

        # ----------------------------------------------------
        # Test PostgreSQL connection
        # ----------------------------------------------------

        self.connection = self.get_connection()

        print("PostgreSQL connected successfully.")


    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def get_connection(self):

        """
        Create a PostgreSQL connection.
        """

        return psycopg2.connect(
            **self.db_config
        )


    # ========================================================
    # CREATE QUERY EMBEDDING
    # ========================================================

    def create_query_embedding(
        self,
        question: str
    ):

        """
        Convert the student's question into
        an embedding vector.
        """

        if not question or not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        # Create embedding for the query
        embedding = self.embedder.embed_query(
            question
        )

        return embedding


    # ========================================================
    # GENERIC SEMANTIC SEARCH
    # ========================================================

    def semantic_search(
        self,
        question: str,
        k: int = DEFAULT_K,
        content_type: str = None,
        topic: str = None,
        difficulty: str = None,
        user_id: int = None,
        file_type: str = None
    ):
        """
        Perform semantic similarity search using pgvector.

        Optional filters:

        content_type:
            dsa
            story
            description
            leetcode
            student_code

        topic:
            Array
            Stack
            Queue
            Tree
            Graph
            etc.

        difficulty:
            Easy
            Medium
            Hard

        user_id:
            Used for retrieving a student's own code.

        file_type:
            py
            ipynb
        """

        # ----------------------------------------------------
        # Create query embedding
        # ----------------------------------------------------

        query_embedding = self.create_query_embedding(
            question
        )


        # ----------------------------------------------------
        # Base SQL query
        # ----------------------------------------------------

        sql = """
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> %s::vector) AS similarity

            FROM rag_chunks

            WHERE 1 = 1
        """


        # Parameters passed to PostgreSQL
        parameters = [
            json.dumps(query_embedding)
        ]


        # ----------------------------------------------------
        # Content type filter
        # ----------------------------------------------------

        if content_type:

            sql += """
                AND metadata->>'content_type' = %s
            """

            parameters.append(
                content_type
            )


        # ----------------------------------------------------
        # Topic filter
        # ----------------------------------------------------

        if topic:

            sql += """
                AND LOWER(metadata->>'topic') = LOWER(%s)
            """

            parameters.append(
                topic
            )


        # ----------------------------------------------------
        # Difficulty filter
        # ----------------------------------------------------

        if difficulty:

            sql += """
                AND LOWER(metadata->>'difficulty') = LOWER(%s)
            """

            parameters.append(
                difficulty
            )


        # ----------------------------------------------------
        # User filter
        # ----------------------------------------------------

        if user_id:

            sql += """
                AND (
                    metadata->>'user_id' = %s
                    OR metadata->>'user_id' IS NULL
                )
            """

            parameters.append(
                str(user_id)
            )


        # ----------------------------------------------------
        # File type filter
        # ----------------------------------------------------

        if file_type:

            sql += """
                AND metadata->>'file_type' = %s
            """

            parameters.append(
                file_type
            )


        # ----------------------------------------------------
        # Similarity ordering
        # ----------------------------------------------------

        sql += """
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """


        # Add embedding again for ORDER BY
        parameters.append(
            json.dumps(query_embedding)
        )

        parameters.append(
            k
        )


        # ----------------------------------------------------
        # Execute query
        # ----------------------------------------------------

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                sql,
                parameters
            )

            rows = cursor.fetchall()

        finally:

            cursor.close()
            connection.close()


        # ----------------------------------------------------
        # Convert database rows to dictionaries
        # ----------------------------------------------------

        documents = []

        for row in rows:

            chunk_id = row[0]
            content = row[1]
            metadata = row[2]
            similarity = float(row[3])

            documents.append(
                {
                    "id": chunk_id,
                    "content": content,
                    "metadata": metadata,
                    "similarity": similarity
                }
            )


        return documents


    # ========================================================
    # RETRIEVE DSA KNOWLEDGE
    # ========================================================

    def retrieve_dsa_knowledge(
        self,
        question: str,
        k: int = 5,
        topic: str = None
    ):
        """
        Retrieve DSA theory, notes and explanations.
        """

        return self.semantic_search(

            question=question,

            k=k,

            topic=topic
        )


    # ========================================================
    # RETRIEVE STORIES
    # ========================================================

    def retrieve_stories(
        self,
        question: str,
        k: int = 2,
        topic: str = None
    ):
        """
        Retrieve real-world stories or analogies
        related to the DSA question.
        """

        return self.semantic_search(

            question=question,

            k=k,

            content_type="story",

            topic=topic
        )


    # ========================================================
    # RETRIEVE DESCRIPTIONS
    # ========================================================

    def retrieve_descriptions(
        self,
        question: str,
        k: int = 2,
        topic: str = None
    ):
        """
        Retrieve concept descriptions.
        """

        return self.semantic_search(

            question=question,

            k=k,

            content_type="description",

            topic=topic
        )


    # ========================================================
    # RETRIEVE LEETCODE QUESTIONS
    # ========================================================

    def retrieve_leetcode(
        self,
        question: str,
        difficulty: str = None,
        topic: str = None,
        k: int = 3
    ):
        """
        Retrieve relevant LeetCode-style questions.

        Example:

        difficulty = "Medium"
        topic = "Sliding Window"
        """

        return self.semantic_search(

            question=question,

            k=k,

            content_type="leetcode",

            topic=topic,

            difficulty=difficulty
        )


    # ========================================================
    # RETRIEVE STUDENT PYTHON CODE
    # ========================================================

    def retrieve_python_code(
        self,
        question: str,
        user_id: int,
        k: int = 3
    ):
        """
        Retrieve student's .py files.
        """

        return self.semantic_search(

            question=question,

            k=k,

            content_type="student_code",

            user_id=user_id,

            file_type="py"
        )


    # ========================================================
    # RETRIEVE STUDENT NOTEBOOK CODE
    # ========================================================

    def retrieve_notebook_code(
        self,
        question: str,
        user_id: int,
        k: int = 3
    ):
        """
        Retrieve student's .ipynb files.
        """

        return self.semantic_search(

            question=question,

            k=k,

            content_type="student_code",

            user_id=user_id,

            file_type="ipynb"
        )


    # ========================================================
    # BUILD DOCUMENT TEXT
    # ========================================================

    def format_documents(
        self,
        documents
    ):
        """
        Convert retrieved documents into readable
        context for the LLM.
        """

        if not documents:

            return (
                "No relevant information was found "
                "in the knowledge base."
            )


        context_parts = []


        for document in documents:

            metadata = document.get(
                "metadata",
                {}
            )

            source = metadata.get(
                "source",
                "Unknown"
            )

            topic = metadata.get(
                "topic",
                "Unknown"
            )

            content_type = metadata.get(
                "content_type",
                "Unknown"
            )

            difficulty = metadata.get(
                "difficulty",
                "N/A"
            )

            similarity = document.get(
                "similarity",
                0
            )


            context_parts.append(
                f"""
Source: {source}
Topic: {topic}
Type: {content_type}
Difficulty: {difficulty}
Similarity: {similarity:.3f}

Content:
{document['content']}
""".strip()
            )


        return "\n\n---\n\n".join(
            context_parts
        )


    # ========================================================
    # MAIN RAG RETRIEVAL
    # ========================================================

    def retrieve_context(
        self,
        question: str,
        k: int = 5,
        topic: str = None,
        difficulty: str = None,
        user_id: int = None,
        include_code: bool = False,
        include_leetcode: bool = True,
        include_stories: bool = True
    ):
        """
        Main retrieval function used by coach.py.

        This function creates a complete RAG context
        for the DSA Coach.
        """

        if not question or not question.strip():

            return (
                "No question was provided."
            )


        all_documents = []


        # ====================================================
        # 1. RETRIEVE DSA KNOWLEDGE
        # ====================================================

        dsa_documents = self.retrieve_dsa_knowledge(

            question=question,

            k=k,

            topic=topic
        )

        all_documents.extend(
            dsa_documents
        )


        # ====================================================
        # 2. RETRIEVE STORIES
        # ====================================================

        if include_stories:

            story_documents = self.retrieve_stories(

                question=question,

                k=2,

                topic=topic
            )

            all_documents.extend(
                story_documents
            )


        # ====================================================
        # 3. RETRIEVE LEETCODE
        # ====================================================

        if include_leetcode:

            leetcode_documents = self.retrieve_leetcode(

                question=question,

                difficulty=difficulty,

                topic=topic,

                k=2
            )

            all_documents.extend(
                leetcode_documents
            )


        # ====================================================
        # 4. RETRIEVE STUDENT CODE
        # ====================================================

        if include_code and user_id:

            # ----------------------------------------------
            # Python files
            # ----------------------------------------------

            python_documents = self.retrieve_python_code(

                question=question,

                user_id=user_id,

                k=2
            )

            all_documents.extend(
                python_documents
            )


            # ----------------------------------------------
            # Jupyter notebooks
            # ----------------------------------------------

            notebook_documents = self.retrieve_notebook_code(

                question=question,

                user_id=user_id,

                k=2
            )

            all_documents.extend(
                notebook_documents
            )


        # ====================================================
        # SORT BY SIMILARITY
        # ====================================================

        all_documents.sort(

            key=lambda x: x.get(
                "similarity",
                0
            ),

            reverse=True
        )


        # ====================================================
        # BUILD FINAL CONTEXT
        # ====================================================

        context = self.format_documents(
            all_documents
        )


        return context


# ============================================================
# CREATE GLOBAL RAG INSTANCE
# ============================================================

rag = DSA_RAG()


# ============================================================
# FUNCTION USED BY coach.py
# ============================================================

def retrieve_context(
    question: str,
    k: int = 5,
    topic: str = None,
    difficulty: str = None,
    user_id: int = None,
    include_code: bool = False,
    include_leetcode: bool = True,
    include_stories: bool = True
):
    """
    Simple function that can be imported
    directly into coach.py.
    """

    return rag.retrieve_context(

        question=question,

        k=k,

        topic=topic,

        difficulty=difficulty,

        user_id=user_id,

        include_code=include_code,

        include_leetcode=include_leetcode,

        include_stories=include_stories
    )
