import requests


BACKEND_API_URL = "http://localhost:8000/api"


def upload_file(file_path):
    with open(file_path,"rb") as f:
        response = requests.post(f"{BACKEND_API_URL}/upload", files={"file": f})
    return response.json()

def chat_with_bot(query):
    response = requests.post(f"{BACKEND_API_URL}/chat", json={"query": query})
    return response.json()