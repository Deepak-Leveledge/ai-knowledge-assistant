from backend.services.retriever import RetrieverService 
from backend.services.generator import generate_response
from backend.database.mongo import save_chat, get_user_docs
from datetime import datetime



class RAGPipeline:
    
    def __init__(self):
        self.retriever = RetrieverService()
        
    def run(self, query):
        docs = self.retriever.get_relevent_documents(query)
        context = "\n".join([str(d) for d in docs])
        answer = generate_response(query, context)
        return {"context": context, "answer": answer}
    
    def run_query(self, query):
        return self.run(query)
    
    def save_chat_history(self, user_id, question, answer):
        try:
            
           save_chat(user_id, question, answer, timestamp=datetime.utcnow())
           return True
        except Exception as e:
            print(f"Failed to save chat: {str(e)}")
            return False
        
        
    def get_user_history(self, user_id):
        return get_user_docs(user_id)