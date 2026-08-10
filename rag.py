import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# CONFIGURATION
# ==========================================

# Path where the FAISS vector database is stored
VECTOR_DB_PATH = "vectorstore/faiss_index"

# Hugging Face embedding model used to convert
# text into numerical vectors
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ==========================================
# RAG RETRIEVER
# ==========================================

class DSA_RAG:
    """
    Retrieval-Augmented Generation (RAG) retrieval layer
    for the DSA Coach Agent.

    This class is responsible for:
    1. Loading the embedding model
    2. Loading the FAISS vector database
    3. Searching for relevant DSA information
    4. Returning the retrieved information as context
    """

    def __init__(
        self,
        vector_db_path: str = VECTOR_DB_PATH
    ):
        # Store the path of the FAISS vector database
        self.vector_db_path = vector_db_path

        # ------------------------------------------
        # Load Embedding Model
        # ------------------------------------------

        print("Loading embedding model...")

        # Load the Hugging Face embedding model
        # This model converts text into vector representations
        self.embedder = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            encode_kwargs={
                # Normalize embeddings for better similarity search
                "normalize_embeddings": True
            }
        )

        print("Embedding model loaded.")

        # ------------------------------------------
        # Load FAISS Vector Database
        # ------------------------------------------

        print("Loading FAISS vector database...")

        # Check whether the FAISS database exists
        if not os.path.exists(self.vector_db_path):
            raise FileNotFoundError(
                f"FAISS vector database not found at "
                f"'{self.vector_db_path}'. "
                f"Run 'python ingest.py' first."
            )

        # Load the previously created FAISS vector database
        self.vectorstore = FAISS.load_local(
            self.vector_db_path,
            self.embedder,

            # Required when loading a locally created
            # FAISS index containing serialized data
            allow_dangerous_deserialization=True
        )

        print("FAISS vector database loaded successfully.")

    # ==========================================
    # RETRIEVE RELEVANT CONTEXT
    # ==========================================

    def retrieve_context(
        self,
        question: str,
        k: int = 4
    ) -> str:

        # Check whether the user provided a question
        if not question or not question.strip():
            return "No question was provided."

        # ------------------------------------------
        # Similarity Search
        # ------------------------------------------

        # Search the FAISS database for the most
        # relevant documents related to the question
        retrieved_documents = self.vectorstore.similarity_search(
            question,
            k=k
        )

        # If no relevant documents are found,
        # return a suitable message
        if not retrieved_documents:
            return (
                "I couldn't find relevant information "
                "in the DSA knowledge base."
            )

        # ------------------------------------------
        # Build Context
        # ------------------------------------------

        # This list will contain the retrieved
        # document information
        context_parts = []

        # Process every retrieved document
        for document in retrieved_documents:

            # Get the source file from metadata
            source = document.metadata.get(
                "source",
                "Unknown"
            )

            # Get the DSA topic from metadata
            topic = document.metadata.get(
                "topic",
                "Unknown"
            )

            # Add source, topic and document content
            # to the context
            context_parts.append(
                f"""
Source: {source}
Topic: {topic}

{document.page_content}
""".strip()
            )

        # Combine all retrieved documents into
        # one context string
        context = "\n\n---\n\n".join(
            context_parts
        )

        return context


# ==========================================
# CREATE RAG INSTANCE
# ==========================================

# Create one instance of the DSA_RAG class
# This loads the embedding model and FAISS database
rag = DSA_RAG()


# ==========================================
# FUNCTION USED BY coach.py
# ==========================================

def retrieve_context(
    question: str,
    k: int = 4
) -> str:

    # Call the RAG class method to retrieve
    # relevant DSA information
    return rag.retrieve_context(
        question,
        k
    )
