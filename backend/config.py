import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vector_store/index.faiss")      