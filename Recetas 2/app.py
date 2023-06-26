from flask import Flask, render_template, request, send_from_directory
import requests

app = Flask(__name__)

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
        recipes = get_recipe(user_input)

        if not recipes:
            message = "No se encontraron recetas con los ingredientes proporcionados."
            recipe_titles = []
        else:
            message = "Recetas recomendadas:"
            recipe_titles = [recipe["title"] for recipe in recipes]

        return render_template("index.html", message=message, recipe_titles=recipe_titles)

    return render_template("index.html")

@app.route("/app.js")
def send_js():
    return send_from_directory("static", "app.js")

if __name__ == "__main__":
    app.run(debug=True)
