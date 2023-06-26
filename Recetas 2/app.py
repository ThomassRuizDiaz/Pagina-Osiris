from flask import Flask, render_template, request, redirect, url_for
from googletrans import Translator
import requests

app = Flask(__name__)

translator = Translator()

def translate_text(text, source_lang, dest_lang):
    translated_text = translator.translate(text, src=source_lang, dest=dest_lang)
    return translated_text.text

def get_recipe(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": "798c2ebae35c49e2b03b15b6ff20d60b",
        "ingredients": ingredients,
        "number": 10,
    }
    response = requests.get(url, params=params)
    recipes = response.json()

    translated_recipes = []
    for recipe in recipes:
        title = translate_text(recipe["title"], "en", "es")
        image_url = recipe["image"]
        recipe_id = recipe["id"]
        translated_recipes.append({"title": title, "image_url": image_url, "recipe_id": recipe_id})

    return translated_recipes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        recipes = get_recipe(user_input)

        if not recipes:
            message = "No se encontraron recetas con los ingredientes proporcionados."
            recipe_data = []
        else:
            message = "Recetas recomendadas:"
            recipe_data = recipes

        return render_template("index.html", message=message, recipe_data=recipe_data)

    return render_template("index.html")

@app.route("/recipe/<recipe_id>")
def show_recipe(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": "798c2ebae35c49e2b03b15b6ff20d60b"
    }
    response = requests.get(url, params=params)
    recipe_info = response.json()

    translated_title = translate_text(recipe_info["title"], "en", "es")
    translated_instructions = translate_text(recipe_info["instructions"], "en", "es")
    recipe_data = {
        "title": translated_title,
        "instructions": translated_instructions
    }

    return render_template("recipe.html", recipe_data=recipe_data)

if __name__ == "__main__":
    app.run(debug=True)
