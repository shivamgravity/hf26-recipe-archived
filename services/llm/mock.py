import os
import json
from services.llm.base import RecipeLLM
from models.recipe import Recipe

class MockGemmaLLM(RecipeLLM):
    def extract_recipe(self, transcript: str) -> Recipe:
        # We return a dummy recipe for testing purposes.
        return Recipe(
            title="Aloo Jeera (Mocked)",
            description="A simple home-style potato recipe extracted from transcript.",
            source_person="Family",
            servings=4,
            prep_time_minutes=10,
            cook_time_minutes=20,
            ingredients=[
                {"item": "potatoes", "quantity": "4", "unit": "medium"},
                {"item": "oil", "quantity": "2", "unit": "tablespoons"},
                {"item": "cumin", "quantity": "1", "unit": "teaspoon"},
                {"item": "salt", "quantity": "to taste", "unit": None}
            ],
            steps=[
                "Heat the oil in a pan.",
                "Add cumin seeds and let them crackle.",
                "Add the potatoes and cook until lightly crisp.",
                "Add salt to taste."
            ],
            tips=[
                "Don't add too much water."
            ],
            original_transcript=transcript
        )
