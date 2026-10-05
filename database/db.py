import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        source_person TEXT,
        servings INTEGER,
        prep_time_minutes INTEGER,
        cook_time_minutes INTEGER,
        original_transcript TEXT,
        audio_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id TEXT,
        item TEXT,
        quantity TEXT,
        unit TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id TEXT,
        step_number INTEGER,
        instruction TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id TEXT,
        tip TEXT,
        FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
