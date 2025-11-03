from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from typing import Any
from dotenv import load_dotenv
load_dotenv()
import os



def get_embeddings_models() -> Any:
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", api_key=os.getenv("GOOGLE_API_KEY"))
