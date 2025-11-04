import requests


BACKEND_API_URL = "https://ai-knowledge-assistant-1-fi2y.onrender.com/api"



def upload_file(file_paths):
    """
    Upload single or multiple files to FastAPI backend.
    file_paths: str | list[str]
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    files_data = [("files", (open(path, "rb"))) for path in file_paths]

    try:
        response = requests.post(f"{BACKEND_API_URL}/upload", files=files_data)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    
    
def chat_with_bot(query):
    response = requests.post(f"{BACKEND_API_URL}/chat", json={"query": query})
    return response.json()