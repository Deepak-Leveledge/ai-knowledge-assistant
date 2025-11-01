from backend.services.vectore_store import VectorStore

class RetrieverService:
    def __init__(self):
        self.vector_store = VectorStore()
        
    def get_relevent_documents(self, query, top_k=5):
        return self.vector_store.search(query, top_k=top_k)