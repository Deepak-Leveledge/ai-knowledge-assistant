from fastapi import APIRouter, HTTPException
from backend.services.langgraph_flow import ChatFlow
from backend.services.rag_pipeline import RAGPipeline
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        chat_flow = RAGPipeline()
        result = chat_flow.run_query(request.query)

        # Assuming result is a dict with 'answer' key
        answer = result.get("answer") if isinstance(result, dict) else result

        # print(f"Chat Answer: {answer}")
        return {"answer": answer}

    except Exception as e:
        print(f"Error in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))