from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from backend.services.vectore_store import VectorStore
from backend.utils.file_utils import save_upload_file
from backend.services.document_processor import load_and_split


router = APIRouter()

@router.post("/upload")
async def upload_file(files: List[UploadFile] = File(...)):
    total_chunks = 0
    processed_files = []
    store = VectorStore()  # Create store once for all files
    
    try:
        for file in files:
            path = save_upload_file(file)
            docs = load_and_split(path)
            store.add_documents(docs)
            total_chunks += len(docs)
            processed_files.append({
                "filename": file.filename,
                "chunks": len(docs)
            })
            
        return {
            "status": "success",
            "message": f"Processed {len(processed_files)} files successfully",
            "total_chunks_added": total_chunks,
            "files": processed_files
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}"
        )