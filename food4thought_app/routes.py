from flask import render_template, url_for, request, redirect
from food4thought_app import app
from food4thought_app.database import db
from datetime import datetime

#skriver ut recepten på startsidan
@app.route('/')
def index():
    recipe_list = []
    sql = sql = "select username, headline, preamble, instructions, published, recipe_ID from recipe"
    db.cursor.execute(sql)

    for recipe in db.cursor:
        recipe_list.append(recipe)

    return render_template("index.html", recipe_list = recipe_list)


@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/register/')
def register():
    return render_template("register.html")

@app.route('/new_recipe/')
def new_recipe():

    return render_template("new_recipe.html")

#tar från formulär för att lägga till recept i databasen

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

#tar data från databasen för att skriva ut det på recipe.html
@app.route('/recipe/<recipe_id>/')
def show_recipe(recipe_id):
    recipe = []
    sql = "select recipe_id, username, headline, preamble, instructions, published from recipe where recipe_id = %s"
    db.cursor.execute(sql,(recipe_id,))

    [recipe.append(i) for recipes in db.cursor for i in recipes ]
    
    return render_template("recipe.html", recipe=recipe)
