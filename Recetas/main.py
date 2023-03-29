from flask import Flask, render_template, request
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
        "number": 3,
    }
    response = requests.get(url, params=params)
    recipes = response.json()
    return recipes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        translated_input = translate_text(user_input, "es", "en")
        recipes = get_recipe(translated_input)

        if not recipes:
            message = "No se encontraron recetas con los ingredientes proporcionados."
        else:
            message = "Recetas recomendadas:"
            recipe_titles = []
            for recipe in recipes:
                recipe_titles.append(recipe["title"])

        return render_template("index.html", message=message, recipe_titles=recipe_titles)

    return render_template("index.html")

@app.route("/send_js")
def send_js():
    return app.send_static_file("app.js")

if __name__ == "__main__":
    app.run(debug=True)
