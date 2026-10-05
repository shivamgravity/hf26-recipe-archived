import uuid
import datetime
from database.db import get_connection
from models.recipe import Recipe, Ingredient

def save_recipe(recipe: Recipe) -> Recipe:
    conn = get_connection()
    cursor = conn.cursor()
    
    if not recipe.id:
        recipe.id = str(uuid.uuid4())
        recipe.created_at = datetime.datetime.now()
    
    recipe.updated_at = datetime.datetime.now()
    
    # Upsert Recipe
    cursor.execute("""
    INSERT OR REPLACE INTO recipes 
    (id, title, description, source_person, servings, prep_time_minutes, cook_time_minutes, original_transcript, audio_path, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recipe.id, recipe.title, recipe.description, recipe.source_person, 
        recipe.servings, recipe.prep_time_minutes, recipe.cook_time_minutes, 
        recipe.original_transcript, recipe.audio_path, recipe.created_at, recipe.updated_at
    ))
    
    # Delete old associated records
    cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe.id,))
    cursor.execute("DELETE FROM steps WHERE recipe_id = ?", (recipe.id,))
    cursor.execute("DELETE FROM tips WHERE recipe_id = ?", (recipe.id,))
    
    # Insert ingredients
    for ing in recipe.ingredients:
        cursor.execute("INSERT INTO ingredients (recipe_id, item, quantity, unit) VALUES (?, ?, ?, ?)",
                       (recipe.id, ing.item, ing.quantity, ing.unit))
                       
    # Insert steps
    for i, step in enumerate(recipe.steps):
        cursor.execute("INSERT INTO steps (recipe_id, step_number, instruction) VALUES (?, ?, ?)",
                       (recipe.id, i + 1, step))
                       
    # Insert tips
    for tip in recipe.tips:
        cursor.execute("INSERT INTO tips (recipe_id, tip) VALUES (?, ?)", (recipe.id, tip))
        
    conn.commit()
    conn.close()
    
    return recipe

def get_all_recipes() -> list[Recipe]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
    recipe_rows = cursor.fetchall()
    
    recipes = []
    for row in recipe_rows:
        recipe_dict = dict(row)
        recipe_id = recipe_dict["id"]
        
        cursor.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = [Ingredient(**dict(r)) for r in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number", (recipe_id,))
        steps = [r["instruction"] for r in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM tips WHERE recipe_id = ?", (recipe_id,))
        tips = [r["tip"] for r in cursor.fetchall()]
        
        recipe_dict["ingredients"] = ingredients
        recipe_dict["steps"] = steps
        recipe_dict["tips"] = tips
        
        recipes.append(Recipe(**recipe_dict))
        
    conn.close()
    return recipes

def search_recipes(query: str) -> list[Recipe]:
    # Simple search
    recipes = get_all_recipes()
    query = query.lower()
    
    result = []
    for r in recipes:
        if query in r.title.lower() or \
           (r.description and query in r.description.lower()) or \
           (r.source_person and query in r.source_person.lower()) or \
           any(query in ing.item.lower() for ing in r.ingredients) or \
           any(query in tip.lower() for tip in r.tips):
            result.append(r)
            
    return result

def delete_recipe(recipe_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
