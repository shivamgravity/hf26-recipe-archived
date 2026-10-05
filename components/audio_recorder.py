import streamlit as st
import tempfile
import os
from services.transcription import get_transcription_provider
from services.llm import get_llm
from components.recipe_editor import render_recipe_editor

def render_audio_upload(go_to):
    st.header("Who is this recipe from?")
    source_person = st.selectbox("Select or type:", ["Dadi", "Nani", "Mom", "Dad", "Grandpa", "Friend", "Other"])
    if source_person == "Other":
        source_person = st.text_input("Enter name:")
        
    st.header("How would you like to add it?")
    
    upload_tab, paste_tab, demo_tab = st.tabs(["📁 Upload Voice Note", "📝 Paste Transcript", "✨ Demo Mode"])
    
    transcript = None
    
    with upload_tab:
        uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "webm", "ogg"])
        if uploaded_file and st.button("Process Audio"):
            st.write("Creating your recipe...")
            st.success("✓ Reading your voice note")
            
            with st.spinner("◉ Transcribing audio..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                    
                try:
                    transcriber = get_transcription_provider()
                    transcript = transcriber.transcribe(tmp_path)
                    st.session_state.temp_transcript = transcript
                    st.success("✓ Transcribing audio")
                except Exception as e:
                    st.error(f"Failed to transcribe: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                
    with paste_tab:
        pasted_text = st.text_area("Paste the spoken transcript here:")
        if st.button("Process Transcript") and pasted_text:
            st.session_state.temp_transcript = pasted_text
            
    with demo_tab:
        st.write("Try a Sample Recipe without uploading audio.")
        sample_transcript = "Beta aaj aloo jeera banaya tha. Pehle chaar aloo ubaal lena. Phir kadhai mein do chamach tel garam karna hai. Usmein jeera daalna hai. Phir thodi si haldi aur namak apne hisaab se. Aloo daal ke achhe se bhunna hai jab tak thode crispy ho jaayein. Zyada paani mat daalna, warna maza nahi aayega."
        st.info(f"Sample: '{sample_transcript}'")
        if st.button("Try Sample"):
            st.session_state.temp_transcript = sample_transcript
            
    if 'temp_transcript' in st.session_state:
        if transcript:  # Only if it was from upload, else we do it implicitly
            pass 
        else:
            st.write("Creating your recipe...")
            
        with st.spinner("◉ Understanding the recipe and organizing ingredients..."):
            try:
                llm = get_llm()
                recipe = llm.extract_recipe(st.session_state.temp_transcript)
                recipe.source_person = source_person
                st.session_state.draft_recipe = recipe
                st.success("✓ Recipe structured successfully")
                del st.session_state.temp_transcript
            except Exception as e:
                st.error(f"We couldn't turn this into a recipe yet. {e}")
                if st.button("Retry"):
                    st.rerun()
            
    if 'draft_recipe' in st.session_state:
        st.write("---")
        st.success("○ Preparing your recipe card")
        st.header("Here's what we understood")
        render_recipe_editor(st.session_state.draft_recipe, go_to)
