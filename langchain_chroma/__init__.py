import os
import json
import numpy as np
from langchain_core.documents import Document

class ChromaRetriever:
    def __init__(self, vectorstore, k=5):
        self.vectorstore = vectorstore
        self.k = k
        
    def invoke(self, query: str) -> list:
        return self.vectorstore.similarity_search(query, k=self.k)

class Chroma:
    def __init__(self, collection_name: str, persist_directory: str, embedding_function):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.db_path = os.path.join(persist_directory, "mock_db.json")
        self.documents = []
        self.embeddings = []
        self.ids = []
        self.load()
        
    def load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.ids = data.get("ids", [])
                    self.embeddings = data.get("embeddings", [])
                    self.documents = [
                        Document(page_content=doc["page_content"], metadata=doc["metadata"])
                        for doc in data.get("documents", [])
                    ]
            except Exception:
                pass
                
    def save(self):
        os.makedirs(self.persist_directory, exist_ok=True)
        doc_data = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in self.documents
        ]
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump({
                "ids": self.ids,
                "embeddings": self.embeddings,
                "documents": doc_data
            }, f, indent=2)
            
    def add_documents(self, documents, ids):
        texts = [doc.page_content for doc in documents]
        new_embeddings = self.embedding_function.embed_documents(texts)
        
        self.documents.extend(documents)
        self.ids.extend(ids)
        self.embeddings.extend(new_embeddings)
        self.save()
        
    def similarity_search(self, query: str, k: int = 5) -> list:
        if not self.embeddings:
            return []
        # Truncate query to 500 characters to prevent Ollama 500 error on extremely long inputs
        query = query[:500]
        query_embedding = self.embedding_function.embed_query(query)
        
        q = np.array(query_embedding)
        db = np.array(self.embeddings)
        
        dot_products = np.dot(db, q)
        norms_db = np.linalg.norm(db, axis=1)
        norm_q = np.linalg.norm(q)
        
        similarities = dot_products / (norms_db * norm_q + 1e-9)
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        return [self.documents[i] for i in top_k_indices]
        
    def as_retriever(self, search_kwargs=None):
        k = 5
        if search_kwargs and "k" in search_kwargs:
            k = search_kwargs["k"]
        return ChromaRetriever(self, k=k)
