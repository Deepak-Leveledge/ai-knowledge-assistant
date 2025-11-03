from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import Config

def generate_response(query,full_context):
    chat_model = ChatGoogleGenerativeAI(api_key=Config.GOOGLE_API_KEY ,model="gemini-2.5-flash", temperature=0)
    prompt = f"Summarize the content below and answer the question.\n\nDocument content:\n{full_context}\n\nQuestion: {query}\n\nSummary / Answer:"
      # ✅ invoke() instead of ()
    response = chat_model.invoke(prompt)
    
    # response is usually a `AIMessage` object
    return response.content if hasattr(response, "content") else str(response)



# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from backend.config import Config

# # instantiate model once
# _chat_model = ChatGoogleGenerativeAI(
#     api_key=Config.GOOGLE_API_KEY,
#     model="gemini-2.5-flash",
#     temperature=0
# )

# def _extract_text_from_gen(gen) -> str:
#     # unwrap tuples like (generation, score) or similar
#     if isinstance(gen, tuple) and len(gen) > 0:
#         gen = gen[0]

#     # dict-style generation
#     if isinstance(gen, dict):
#         if gen.get("text"):
#             return gen["text"]
#         msg = gen.get("message")
#         if isinstance(msg, dict):
#             return msg.get("content", "")
#         if hasattr(msg, "content"):
#             return getattr(msg, "content", "")

#     # object-style generation
#     if getattr(gen, "text", None):
#         return gen.text
#     if getattr(gen, "message", None):
#         msg = gen.message
#         if isinstance(msg, dict):
#             return msg.get("content", "")
#         if getattr(msg, "content", None):
#             return msg.content

#     return ""

# def generate_response(query: str, context: str) -> str:
#     prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
#     result = _chat_model.generate([HumanMessage(content=prompt)])
#     # guard against unexpected shapes
#     try:
#         gen = result.generations[0][0]
#     except Exception:
#         # fallback: try first available element
#         try:
#             gen = result.generations[0]
#         except Exception:
#             return ""
#     return _extract_text_from_gen(gen)