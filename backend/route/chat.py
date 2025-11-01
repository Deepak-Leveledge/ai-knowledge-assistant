from fastapi import APIRouter, HTTPException
from backend.services.langgraph_flow import ChatFlow
from backend.services.rag_pipeline import RAGPipeline

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(query: str):
    try:
        chat_flow = RAGPipeline()
        result = chat_flow.run_query(query)
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"Error in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))