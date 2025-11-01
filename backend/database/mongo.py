from pymongo import MongoClient
from backend.config import Config

# Create a MongoDB client
client = MongoClient(Config.MONGODB_URI)

# connect to the database wirh data base name knowledge_assistant
db = client["knowledge_assistant"]

def save_chat(user_id,question,answer):
    db.chats.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer
    })


def get_user_docs(user_id):
    return list(db.chats.find({"user_id": user_id}))

