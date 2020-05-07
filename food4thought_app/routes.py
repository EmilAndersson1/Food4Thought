from flask import render_template, url_for, request, redirect
from food4thought_app import app
from food4thought_app.database import db
from datetime import datetime
from random import randint

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
 

@app.route('/generator/')
def generator():

    return render_template("generator.html")

@app.route('/generator-number/', methods=['POST'])
def gen_number():
    number = request.form["number"]
    recipe_list = []
    psql = "select * from recipe where recipe_id = %s"
    amount_of_recipes = "select count(*) from recipe"
    db.cursor.execute(amount_of_recipes)
    amount = db.cursor.fetchone()
    lmao = ""
    for a in amount:
        lmao = a
    random_numbers = []
    for i in range(int(number)):
        random_numbers.append(randint(0, lmao))
    for i in random_numbers:
        db.cursor.execute(psql,(i,))
        for recipe in db.cursor:
            recipe_list.append(list(recipe))
            
    print(recipe_list)
    return redirect(url_for("matsedel", recipe_list = recipe_list))

@app.route('/matsedel/')
def matsedel():
    
    return render_template("matsedel.html", recipe = request.args.get("recipe_list"))