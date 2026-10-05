import os
from services.llm.base import RecipeLLM

def get_llm() -> RecipeLLM:
    provider = os.environ.get("LLM_PROVIDER", "ollama").lower()
    
    if provider == "ollama":
        try:
            from services.llm.ollama_gemma import OllamaGemmaLLM
            return OllamaGemmaLLM()
        except ImportError as e:
            import logging
            logging.error(f"Could not load Ollama provider ({e}). Falling back to mock.")
            from services.llm.mock import MockGemmaLLM
            return MockGemmaLLM()
    else:
        from services.llm.mock import MockGemmaLLM
        return MockGemmaLLM()
