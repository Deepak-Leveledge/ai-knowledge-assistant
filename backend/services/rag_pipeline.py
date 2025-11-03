from backend.services.retriever import RetrieverService 
from backend.services.generator import generate_response
from backend.database.mongo import save_chat, get_user_docs
from datetime import datetime



class RAGPipeline:
    
    def __init__(self):
        self.retriever = RetrieverService()
        
    def run(self, query):
        docs = self.retriever.get_relevent_documents(query)

        # Build context from actual text when available, fallback to dict fields or str()
        context_parts = []
        for d in docs:
            if hasattr(d, "page_content") and d.page_content:
                context_parts.append(d.page_content)
            elif isinstance(d, dict):
                # common keys that might contain text
                for key in ("text", "content", "page_content"):
                    if key in d and d[key]:
                        context_parts.append(d[key])
                        break
                else:
                    context_parts.append(str(d))  # last resort
            else:
                context_parts.append(str(d))

        # join and optionally truncate long context
        full_context = "\n\n".join(context_parts)
        max_chars = 20000  # adjust as needed
        if len(full_context) > max_chars:
            full_context = full_context[:max_chars] + "\n\n[...truncated...]"

        # give the model a clear instruction to summarize document content
        prompt = f"Summarize the content below and answer the question.\n\nDocument content:\n{full_context}\n\nQuestion: {query}\n\nSummary / Answer:"
        answer = generate_response(query, prompt)  # or generate_response(prompt) depending on your generator signature

        return {"context": full_context, "answer": answer}
    
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