import os
import json
import requests
import logging
from services.llm.base import RecipeLLM
from models.recipe import Recipe

class OllamaGemmaLLM(RecipeLLM):
    def __init__(self):
        self.host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.environ.get("GEMMA_MODEL", "gemma3:4b")
        self.prompt_template_path = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "recipe_extraction.txt")
        
        with open(self.prompt_template_path, 'r', encoding='utf-8') as f:
            self.prompt_template = f.read()

    def extract_recipe(self, transcript: str) -> Recipe:
        prompt = self.prompt_template.replace("{transcript}", transcript)
        
        logging.info(f"Sending extraction request to Ollama ({self.model}) at {self.host}")
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1 # Low temperature for more deterministic JSON
                    }
                },
                timeout=600  # Increased to 10 minutes for slower laptops / initial model load
            )
            response.raise_for_status()
            result = response.json()
            raw_text = result.get("response", "")
            
            # Clean and parse JSON
            parsed_data = self._parse_json_safely(raw_text)
            recipe = Recipe(**parsed_data)
            recipe.original_transcript = transcript
            return recipe
            
        except Exception as e:
            logging.error(f"Failed to generate recipe via Ollama: {e}")
            raise RuntimeError(f"Ollama extraction failed: {e}")

    def _parse_json_safely(self, text: str) -> dict:
        text = text.strip()
        # In case the model wrapped it in markdown code blocks despite format: json
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from model output: {text}")
            raise ValueError(f"Model returned invalid JSON: {e}")
