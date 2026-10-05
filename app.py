import streamlit as st
import os
import requests
from database.db import init_db
from database.repository import get_all_recipes
from components.recipe_card import display_recipe
from components.audio_recorder import render_audio_upload
from components.cookbook import render_cookbook

# Configure the app
st.set_page_config(
    page_title="Dadi's Rasoi",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Custom CSS for a warm, personal feel
st.markdown("""
<style>
    .stApp {
        background-color: #fdfbf7;
        color: #4a3f35;
    }
    h1, h2, h3 {
        color: #d35400;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: #d35400;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e67e22;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def check_ai_status():
    st.sidebar.title("AI Configuration")
    
    transcription_provider = os.environ.get("TRANSCRIPTION_PROVIDER", "local").lower()
    llm_provider = os.environ.get("LLM_PROVIDER", "ollama").lower()
    
    st.sidebar.markdown("**Speech recognition**")
    if transcription_provider == "local":
        try:
            import faster_whisper
            st.sidebar.success("● Local — faster-whisper")
        except ImportError:
            st.sidebar.error("⚠ faster-whisper is not installed. Using Mock.")
    else:
        st.sidebar.info("● Mock provider")

    st.sidebar.markdown("**Recipe understanding**")
    if llm_provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        model = os.environ.get("GEMMA_MODEL", "gemma3:4b")
        try:
            r = requests.get(host, timeout=2)
            if r.status_code == 200:
                # Check if model is pulled
                r_tags = requests.get(f"{host}/api/tags", timeout=2)
                models = [m['name'] for m in r_tags.json().get('models', [])]
                if any(model in m for m in models):
                    st.sidebar.success(f"● Local — Gemma via Ollama")
                else:
                    st.sidebar.warning(f"⚠ Ollama running, but '{model}' is missing.")
            else:
                st.sidebar.error("⚠ Ollama returned an error.")
        except requests.exceptions.RequestException:
            st.sidebar.error("⚠ Ollama is not running.")
    else:
        st.sidebar.info("● Mock provider")
        
    st.sidebar.markdown("**Storage**")
    st.sidebar.success("● Local — SQLite")
    
    st.sidebar.markdown("**Internet required**")
    st.sidebar.markdown("No, after model setup")

def main():
    check_ai_status()
    
    st.title("Dadi's Rasoi ❤️")
    
    # Check if purely local
    transcription_provider = os.environ.get("TRANSCRIPTION_PROVIDER", "local").lower()
    llm_provider = os.environ.get("LLM_PROVIDER", "ollama").lower()
    if transcription_provider == "local" and llm_provider == "ollama":
        st.info("🔒 **Local AI**: Your voice recording and recipe stay on this device while Dadi's Rasoi processes them locally.")
        
    st.markdown("**Your family's recipes shouldn't disappear into old voice notes.**")
    
    # Simple Navigation via Session State
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'landing'
        
    def go_to(view):
        st.session_state.current_view = view
        
    if st.session_state.current_view == 'landing':
        st.write("> Turn a family member's spoken recipe into a beautiful, searchable recipe card.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎙️ Add a Recipe", use_container_width=True):
                go_to('add')
                st.rerun()
        with col2:
            if st.button("📖 Open Cookbook", use_container_width=True):
                go_to('cookbook')
                st.rerun()
                
    elif st.session_state.current_view == 'add':
        if st.button("← Back"):
            go_to('landing')
            st.rerun()
        render_audio_upload(go_to)
        
    elif st.session_state.current_view == 'cookbook':
        if st.button("← Home"):
            go_to('landing')
            st.rerun()
        render_cookbook(go_to)

if __name__ == "__main__":
    main()
