from langchain_core.language_models.llms import LLM
from typing import Any, List, Optional
import requests

class OllamaLLM(LLM):
    model: str
    
    @property
    def _llm_type(self) -> str:
        return "ollama_llm"
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
