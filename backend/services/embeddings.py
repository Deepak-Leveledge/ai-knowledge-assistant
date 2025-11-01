from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from typing import Any


def get_embeddings_models() -> Any:
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")