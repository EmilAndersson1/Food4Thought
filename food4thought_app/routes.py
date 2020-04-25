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

@app.route('/login_user/', methods=['POST'])
def login_user():
    email = request.form["email"]
    user_password = request.form["user_password"]

    sql= "select email, user_password from users where email = %s and user_password = %s"
    sql_list = []
    db.cursor.execute(sql, (email, user_password))
    for item in db.cursor:
        for i in item:
            sql_list.append(i)

    input_list = []

    input_list.append(email)
    input_list.append(user_password)

    print(input_list)
    print(sql_list)

    if input_list==sql_list:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/register/')
def register():
    return render_template("register.html")

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
