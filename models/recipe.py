from typing import List, Optional
from pydantic import BaseModel, Field
import datetime

class Ingredient(BaseModel):
    item: str
    quantity: Optional[str] = None
    unit: Optional[str] = None

class Recipe(BaseModel):
    id: Optional[str] = None
    title: str = "Untitled Recipe"
    description: Optional[str] = None
    source_person: Optional[str] = "Family"
    servings: Optional[int] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    ingredients: List[Ingredient] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)
    original_transcript: Optional[str] = None
    audio_path: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
