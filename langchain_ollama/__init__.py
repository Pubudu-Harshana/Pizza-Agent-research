from langchain_ollama.llms import OllamaLLM

class OllamaEmbeddings:
    def __init__(self, model: str):
        self.model = model
        
    def embed_documents(self, texts: list) -> list:
        import requests
        embeddings = []
        for text in texts:
            response = requests.post(
                "http://127.0.0.1:11434/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                }
            )
            response.raise_for_status()
            embeddings.append(response.json()["embedding"])
        return embeddings
        
    def embed_query(self, text: str) -> list:
        import requests
        response = requests.post(
            "http://127.0.0.1:11434/api/embeddings",
            json={
                "model": self.model,
                "prompt": text
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]
