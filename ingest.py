from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==========================================
# CONFIG
# ==========================================

DATA_PATH = Path("data/arrays.md")
VECTOR_DB_PATH = "vectorstore/faiss_index"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ==========================================
# 1. LOAD DOCUMENT
# ==========================================

print("Loading document...")

text = DATA_PATH.read_text(
    encoding="utf-8"
)

print(f"Characters: {len(text)}")


# ==========================================
# 2. CREATE LANGCHAIN DOCUMENT
# ==========================================

document = Document(
    page_content=text,
    metadata={
        "source": str(DATA_PATH),
        "topic": "arrays"
    }
)

documents = [document]

print(
    f"Documents loaded: {len(documents)}"
)


# ==========================================
# 3. CHUNK DOCUMENT
# ==========================================

print("\nSplitting document...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n# ",
        "\n## ",
        "\n### ",
        "\n\n",
        "\n",
        " ",
        ""
    ]
)

chunks = text_splitter.split_documents(
    documents
)

print(
    f"Created {len(chunks)} chunks"
)


# ==========================================
# 4. ADD METADATA
# ==========================================

for i, chunk in enumerate(chunks):

    chunk.metadata["chunk_id"] = i
    chunk.metadata["topic"] = "arrays"


# ==========================================
# 5. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={
        "normalize_embeddings": True
    }
)

print("Embedding model loaded.")


# ==========================================
# 6. CREATE FAISS VECTOR DATABASE
# ==========================================

print("\nCreating FAISS vector database...")

vector_db = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

print("FAISS database created.")


# ==========================================
# 7. SAVE FAISS DATABASE
# ==========================================

Path(VECTOR_DB_PATH).mkdir(
    parents=True,
    exist_ok=True
)

vector_db.save_local(
    VECTOR_DB_PATH
)

print("\n========================================")
print("SUCCESS!")
print("========================================")

print(
    f"FAISS database saved at: "
    f"{VECTOR_DB_PATH}"
)

print(
    f"Total chunks indexed: {len(chunks)}"
)