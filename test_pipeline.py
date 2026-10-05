import os
import sys

# Test 1: Mock pipeline
print("=== Testing Mock Pipeline ===")
os.environ["TRANSCRIPTION_PROVIDER"] = "mock"
os.environ["LLM_PROVIDER"] = "mock"

from services.transcription import get_transcription_provider
from services.llm import get_llm
from models.recipe import Recipe

t_mock = get_transcription_provider()
transcript = t_mock.transcribe("dummy.mp3")
print("Transcript:", transcript)

l_mock = get_llm()
recipe = l_mock.extract_recipe(transcript)
print("Recipe Title:", recipe.title)
print("Recipe Ingredients:", [i.item for i in recipe.ingredients])
print("Mock Pipeline OK\\n")

# Test 2: Local providers (Imports only)
print("=== Testing Local Imports ===")
os.environ["TRANSCRIPTION_PROVIDER"] = "local"
os.environ["LLM_PROVIDER"] = "ollama"

try:
    from services.transcription.faster_whisper import FasterWhisperProvider
    print("FasterWhisperProvider imported successfully")
except ImportError as e:
    print("Failed to import FasterWhisperProvider:", e)

try:
    from services.llm.ollama_gemma import OllamaGemmaLLM
    print("OllamaGemmaLLM imported successfully")
except ImportError as e:
    print("Failed to import OllamaGemmaLLM:", e)

print("\\nTesting complete.")
