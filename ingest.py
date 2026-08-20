from pathlib import Path
import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from database import get_connection, initialize_database
from config import EMBEDDING_MODEL


# ==========================================
# CONFIGURATION
# ==========================================

DATA_PATH = Path("data/notes")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


# ==========================================
# LOAD DOCUMENTS
# ==========================================

def load_documents():

    documents = []

    md_files = list(DATA_PATH.glob("*.md"))

    print(f"Found {len(md_files)} markdown files.")

    for file_path in md_files:

        print(f"Loading: {file_path}")

        text = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            page_content=text,
            metadata={
                "content_type": "dsa",
                "topic": file_path.stem,
                "source": str(file_path),
                "file_type": "md"
            }
        )

        documents.append(document)

    return documents


# ==========================================
# CREATE CHUNKS
# ==========================================

def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = i

    print(f"Created {len(chunks)} chunks.")

    return chunks


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

def create_embedding_model():

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    print("Embedding model loaded.")

    return embeddings


# ==========================================
# STORE IN POSTGRESQL
# ==========================================

def store_chunks(chunks, embeddings):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # Remove previous RAG data
        cursor.execute(
            "TRUNCATE TABLE rag_chunks RESTART IDENTITY;"
        )

        print("Old RAG data cleared.")

        for i, chunk in enumerate(chunks):

            print(
                f"Embedding chunk {i + 1}/{len(chunks)}"
            )

            embedding = embeddings.embed_query(
                chunk.page_content
            )

            metadata = {
                "content_type": chunk.metadata.get(
                    "content_type",
                    "dsa"
                ),
                "topic": chunk.metadata.get(
                    "topic",
                    "unknown"
                ),
                "source": chunk.metadata.get(
                    "source",
                    "unknown"
                ),
                "file_type": chunk.metadata.get(
                    "file_type",
                    "md"
                ),
                "chunk_id": chunk.metadata.get(
                    "chunk_id",
                    i
                )
            }

            cursor.execute(
                """
                INSERT INTO rag_chunks
                (
                    content,
                    metadata,
                    embedding
                )
                VALUES (%s, %s, %s)
                """,
                (
                    chunk.page_content,
                    json.dumps(metadata),
                    embedding
                )
            )

        conn.commit()

        print()
        print("==========================================")
        print("SUCCESS")
        print("==========================================")
        print(f"Stored {len(chunks)} chunks.")
        print("Embeddings stored in PostgreSQL.")
        print("FAISS is NOT being used.")

        cursor.close()

    except Exception as e:

        conn.rollback()

        print("Failed to store RAG data:")
        print(e)

    finally:

        conn.close()


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print("==========================================")
    print("DSA COACH - PostgreSQL RAG INGESTION")
    print("==========================================")
    print()

    initialize_database()

    documents = load_documents()

    if not documents:
        print("No markdown files found.")
        return

    chunks = create_chunks(documents)

    embeddings = create_embedding_model()

    store_chunks(
        chunks,
        embeddings
    )


if __name__ == "__main__":
    main()