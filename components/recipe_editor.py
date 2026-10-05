import streamlit as st
from models.recipe import Recipe, Ingredient
from database.repository import save_recipe
from components.recipe_card import display_recipe

def render_recipe_editor(recipe: Recipe, go_to):
    display_recipe(recipe)
    
    st.write("---")
    st.subheader("Edit Recipe")
    
    with st.form("recipe_editor_form"):
        new_title = st.text_input("Title", value=recipe.title)
        new_desc = st.text_area("Description", value=recipe.description or "")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_servings = st.number_input("Servings", value=recipe.servings or 1)
        with col2:
            new_prep = st.number_input("Prep Time (min)", value=recipe.prep_time_minutes or 0)
        with col3:
            new_cook = st.number_input("Cook Time (min)", value=recipe.cook_time_minutes or 0)
            
        st.markdown("**(Editing ingredients and steps is simplified for MVP. Edit the raw text if needed)**")
        
        # Simplified string editing for MVP
        ings_str = "\n".join([f"{i.quantity or ''} {i.unit or ''} {i.item}".strip() for i in recipe.ingredients])
        new_ings_raw = st.text_area("Ingredients (one per line)", value=ings_str)
        
        steps_str = "\n".join(recipe.steps)
        new_steps_raw = st.text_area("Steps (one per line)", value=steps_str)
        
        tips_str = "\n".join(recipe.tips)
        new_tips_raw = st.text_area("Tips (one per line)", value=tips_str)
        
        if st.form_submit_button("💾 Save to Cookbook"):
            # Update recipe
            recipe.title = new_title
            recipe.description = new_desc
            recipe.servings = int(new_servings) if new_servings else None
            recipe.prep_time_minutes = int(new_prep) if new_prep else None
            recipe.cook_time_minutes = int(new_cook) if new_cook else None
            
            # Simple parse
            recipe.ingredients = []
            for line in new_ings_raw.split("\n"):
                if line.strip():
                    recipe.ingredients.append(Ingredient(item=line.strip()))
                    
            recipe.steps = [s.strip() for s in new_steps_raw.split("\n") if s.strip()]
            recipe.tips = [t.strip() for t in new_tips_raw.split("\n") if t.strip()]
            
            save_recipe(recipe)
            del st.session_state.draft_recipe
            st.success("Recipe saved!")
            go_to('cookbook')
            st.rerun()
