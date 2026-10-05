import streamlit as st
from database.repository import get_all_recipes, search_recipes, delete_recipe
from components.recipe_card import display_recipe

def render_cookbook(go_to):
    st.header("❤️ Our Cookbook")
    st.markdown("> Recipes worth remembering.")
    
    search_query = st.text_input("🔍 Search recipes...")
    
    if search_query:
        recipes = search_recipes(search_query)
    else:
        recipes = get_all_recipes()
        
    if not recipes:
        st.info("No recipes found. Start by adding one!")
        return
        
    if 'selected_recipe_id' in st.session_state:
        recipe = next((r for r in recipes if r.id == st.session_state.selected_recipe_id), None)
        if recipe:
            if st.button("← Back to Cookbook"):
                del st.session_state.selected_recipe_id
                st.rerun()
                
            display_recipe(recipe)
            
            if st.button("🗑️ Delete Recipe"):
                delete_recipe(recipe.id)
                del st.session_state.selected_recipe_id
                st.success("Recipe deleted.")
                st.rerun()
            return

    # Grid layout for cards
    cols = st.columns(2)
    for i, recipe in enumerate(recipes):
        with cols[i % 2]:
            st.markdown(f"### {recipe.title}")
            st.markdown(f"From **{recipe.source_person}**")
            st.caption(f"{len(recipe.ingredients)} ingredients · {len(recipe.steps)} steps")
            if st.button("View Recipe →", key=f"view_{recipe.id}"):
                st.session_state.selected_recipe_id = recipe.id
                st.rerun()
            st.markdown("---")
