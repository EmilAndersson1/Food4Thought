from flask import render_template, url_for, request, redirect
from food4thought_app import app
from food4thought_app.database import db
from datetime import datetime


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_recipe/')
def new_recipe():

    return render_template("new_recipe.html")

@app.route('/add_recipe/', methods=['POST'])
def add_recipe():
    now = datetime.now()
    title = request.form["title"]
    description = request.form["description"]
    instructions = request.form["instructions"]
    time_published = now.strftime("%Y-%m-%d %H:%M")
    
    sql = "INSERT INTO recipe VALUES (DEFAULT, DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (title, description, instructions, time_published))
    db.conn.commit()

    return redirect(url_for("index"))


@app.route('/recipe/<recipe_ID>/')
def show_recipe(recipe_ID):
    recipe = []
    sql = "select recipe_ID, username, headline, preamble, instructions, published from recipe where recipe_ID = %s"
    db.cursor.execute(sql,(recipe_ID,))

    [recipe.append(i) for recipes in db.cursor for i in recipes ]
    
    return render_template("recipe.html", recipe=recipe)