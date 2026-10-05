import streamlit as st
from models.recipe import Recipe

def display_recipe(recipe: Recipe):
    st.markdown(f"## 🥔 {recipe.title}")
    st.markdown(f"**From {recipe.source_person} ❤️**")
    
    if recipe.description:
        st.markdown(f"> {recipe.description}")
        
    meta_info = []
    if recipe.prep_time_minutes:
        meta_info.append(f"Prep: {recipe.prep_time_minutes} min")
    if recipe.cook_time_minutes:
        meta_info.append(f"Cook: {recipe.cook_time_minutes} min")
    if recipe.servings:
        meta_info.append(f"Serves: {recipe.servings}")
        
    if meta_info:
        st.markdown(" · ".join(meta_info))
        
    st.markdown("### Ingredients")
    for ing in recipe.ingredients:
        line = f"- {ing.item}"
        if ing.quantity:
            line += f" ({ing.quantity}"
            if ing.unit:
                line += f" {ing.unit}"
            line += ")"
        st.markdown(line)
        
    st.markdown("### Method")
    for i, step in enumerate(recipe.steps):
        st.markdown(f"**{i+1}.** {step}")
        
    if recipe.tips:
        st.markdown(f"### ❤️ {recipe.source_person}'s Tip")
        for tip in recipe.tips:
            st.markdown(f"> {tip}")
            
    with st.expander("Original Transcript"):
        if recipe.original_transcript:
            st.write(recipe.original_transcript)
        else:
            st.write("No transcript available.")
