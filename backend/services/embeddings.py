from langchain_google_genai import GoogleGenerativeAIEmbeddings 

def get_embeddings_models():
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")