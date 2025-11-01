from fastapi import FastAPI
from backend.route import chat, upload

app = FastAPI(title="AI Knowledge Assistant")

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
