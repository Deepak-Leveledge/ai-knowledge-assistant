from langgraph.graph import StateGraph
from backend.services.rag_pipeline import RAGPipeline

class ChatFlow(StateGraph):
    def __init__(self):
        super().__init__(state_schema={})
        self.rag = RAGPipeline()

    
    def run_query(self, query: str):
        """Run the RAG pipeline for the given query and return result."""
        return self.rag.run(query)