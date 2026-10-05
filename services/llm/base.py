from abc import ABC, abstractmethod
from models.recipe import Recipe

class RecipeLLM(ABC):
    @abstractmethod
    def extract_recipe(self, transcript: str) -> Recipe:
        pass
