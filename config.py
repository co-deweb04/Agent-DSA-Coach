import os
from dotenv import load_dotenv

load_dotenv("key.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_NAME = os.getenv("DB_NAME", "dsa_coach")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# RAG
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# BGE-small produces 384-dimensional vectors
EMBEDDING_DIMENSION = 384

# Number of chunks to retrieve
TOP_K = 4