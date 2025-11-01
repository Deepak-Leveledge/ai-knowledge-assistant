from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.vectore_store import VectorStore
from backend.utils.file_utils import save_upload_file
from backend.services.document_processor import load_and_split


router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = save_upload_file(file)
    docs = load_and_split(path)
    store = VectorStore()
    store.add_documents(docs)
    return {"status":"success", "message":"File uploaded and processed successfully.",
            "chunks_added": len(docs)   }
