import faiss
import numpy as np
import os
import pickle
from backend.services.embeddings import get_embeddings_models
from backend.config import Config

class VectorStore:
    def __init__(self):
        self.model = get_embeddings_models()
        self.index_path = Config.VECTOR_DB_PATH
        self.index = None
        self.metadata = []
        
        
        if os.path.exists(self.index_path):
            self.load_index()
            
    def _ensure_index_dir(self):
        dirpath = os.path.dirname(self.index_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

            
    def load_index(self):
        with open(self.index_path + ".pkl","rb") as f:
            self.metadata = pickle.load(f)
        self.index = faiss.read_index(self.index_path)
        
        
    def save_index(self):
        self._ensure_index_dir()
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def add_documents(self, docs):
        texts = [d.page_content for d in docs]
        embeddings = np.array(self.model.embed_documents(texts))
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.metadata.extend([d.metadata for d in docs])
        self.save_index()

    def search(self, query, top_k=3):
        q_emb = np.array(self.model.embed_documents([query]))
        D, I = self.index.search(q_emb, top_k)
        return [self.metadata[i] for i in I[0]]