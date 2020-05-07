from flask import render_template, url_for, request, redirect
from food4thought_app import app
from food4thought_app.database import db
from datetime import datetime


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

@app.route('/add_recipe/', methods=['POST'])
def add_recipe():
    x = 1
    now = datetime.now()
    title = request.form["title"]
    description = request.form["description"]
    instructions = request.form["instructions"]
    time_published = now.strftime("%Y-%m-%d %H:%M")
    sql = "INSERT INTO recipe VALUES (DEFAULT, DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (title, description, instructions, time_published))

    ingredient_name = request.form["ingredient_name"]
    volume = request.form["volume"]
    measurement = request.form["measurement"]

    while request.form["ingredient_name{}".format(x)] != "":
        ingredient_name = request.form["ingredient_name{}".format(x)]
        volume = request.form["volume{}".format(x)]
        measurement = request.form["measurement{}".format(x)]
        sql2 = "INSERT INTO ingredient_in_recipe VALUES (%s, DEFAULT, %s, %s)"
        db.cursor.execute(sql2, (ingredient_name, volume, measurement))
        db.conn.commit()

    return redirect(url_for("index"))


@app.route('/recipe/<recipe_ID>/')
def show_recipe(recipe_ID):
    recipe = []
    sql = "select recipe_ID, username, headline, preamble, instructions, published from recipe where recipe_ID = %s"
    db.cursor.execute(sql,(recipe_ID,))

    [recipe.append(i) for recipes in db.cursor for i in recipes ]
    
    return render_template("recipe.html", recipe=recipe)
