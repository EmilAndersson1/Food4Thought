from flask import render_template, url_for, request, redirect, session, flash
from food4thought_app import app
from food4thought_app.database import db
from datetime import datetime
import time

import os
from random import randint
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    recipe_list = []
    sql = "select username, title, recipe_description, instructions, time_published, recipe_ID, image_url from recipe"
    db.cursor.execute(sql)

    
    for recipe in db.cursor:
        recipe_list.append(recipe) 

    return render_template("index.html", recipe_list = recipe_list)

@app.route('/profile/')
def profile():
    user_email = ""
    if "user_email" in session:
        email = session["user_email"]
        firstname = session["user_firstname"]
        lastname = session["user_lastname"]
        profile_pic = session["profile_pic"]

    return render_template("profile.html", firstname=firstname, lastname = lastname, email=email, profile_pic = profile_pic)


@app.route('/log_out/')
def log_out():
    session.clear()
    return redirect(url_for("index"))


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user_password = request.form['password']

        sql= "select email, firstname, lastname, user_password, image_url from users where email = %s and user_password = %s"
        db.cursor.execute(sql, (email, user_password))
        user = db.cursor.fetchone()

        if user is None:
            flash("Kombinationen finns inte i vår databas, försök igen.")
        else:
            session["user_email"]=user[0]
            session["user_firstname"]=user[1]
            session["user_lastname"]=user[2]
            session["profile_pic"]=user[4]
            session["logged_in"]=True
            return redirect(url_for('profile'))
    return render_template("login.html")

@app.route('/register/')
def register():
    return render_template("register.html")

@app.route('/add-user/', methods=['POST'])
def add_user():
    email = request.form["email"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    password = request.form["password"]

    image_url = "default.jpg"

    sql= "insert into users(email, firstname, lastname, user_password, image_url) values (%s,%s,%s,%s,%s)"

    db.cursor.execute(sql, (email, firstname, lastname, password, image_url))
    db.conn.commit()
    user = []
    user.append(email)
    user.append(firstname)
    user.append(lastname)
    user.append(image_url)
    session["user_email"]=user[0]
    session["user_firstname"]=user[1]
    session["user_lastname"]=user[2]
    session["profile_pic"]= user[3]
    session["logged_in"]=True

    return redirect(url_for("index"))


@app.route('/new_recipe/')
def new_recipe():

    return render_template("new_recipe.html")

UPLOAD_FOLDER_RECIPE = "food4thought_app/static/recipe_images/"
app.config['UPLOAD_FOLDER_RECIPE'] = UPLOAD_FOLDER_RECIPE

#tar från formulär för att lägga till recept i databasen
@app.route('/add_recipe/', methods=['POST'])
def add_recipe():
    x = 1
    now = datetime.now()
    title = request.form["title"]
    recipe_description = request.form["description"]
    instructions = request.form["instructions"]
    time_published = now.strftime("%Y-%m-%d %H:%M")
    user = session["user_email"]
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], image.filename))
    sql = "INSERT INTO recipe VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"
    db.cursor.execute(sql, (user, title, recipe_description, instructions, time_published, image.filename))

    ingredient_name = request.form["ingredient_name1"]
    volume = request.form["volume1"]
    measurement = request.form["measurement1"]
    ingredienser = []

    while True:
        try:
            ingredient_name = request.form["ingredient_name{}".format(x)]
            volume = request.form["volume{}".format(x)]
            measurement = request.form["measurement{}".format(x)]
            sql2 = "INSERT INTO ingredient VALUES (DEFAULT, %s, %s, %s)"
            db.cursor.execute(sql2, (ingredient_name, volume, measurement))
            db.conn.commit()
            sql3= "select ingredient_id from ingredient order by ingredient_id desc limit 1"
            db.cursor.execute(sql3)
            db.conn.commit()
            for ingrediens in db.cursor:
                ingredienser.append(ingrediens)
            print(ingredienser)
            x += 1
        except:
            break

    for ingrediens in ingredienser:
        sql4 = "INSERT INTO ingredient_in_recipe(recipe_id, ingredient_id) select recipe_id, %s from recipe where title = %s and recipe_description = %s and instructions = %s and time_published = %s"
        db.cursor.execute(sql4,(ingrediens, title, recipe_description, instructions, time_published))
    db.conn.commit()

    return redirect(url_for("index"))

#tar data från databasen för att skriva ut det på recipe.html
@app.route('/recipe/<recipe_id>/')
def show_recipe(recipe_id):

    recipe = []
    sql = "select recipe_id, username, title, recipe_description, instructions, time_published, image_url from recipe where recipe_id = %s"
    db.cursor.execute(sql,(recipe_id,))

    [recipe.append(i) for recipes in db.cursor for i in recipes ]
    
    comments = []
    sql2 = "select comment.username, comment.comment, comment.curr_time, comment.comment_ID, comment.recipe_ID \
            from comment join recipe \
                on recipe.recipe_ID = comment.recipe_ID \
            where recipe.recipe_ID = %s order by comment.curr_time DESC"    
    db.cursor.execute(sql2,(recipe_id,))
    for comment in db.cursor:
        comments.append(comment)

    ingredients = []
    sql3 = "select ingredient.ingredient_name, ingredient.volume, ingredient.measurement\
            from ingredient join ingredient_in_recipe \
                on ingredient_in_recipe.ingredient_id = ingredient.ingredient_id \
            where ingredient_in_recipe.recipe_id = %s"  
    db.cursor.execute(sql3,(recipe_id,))
    for ingredient in db.cursor:
        ingredients.append(ingredient)
      
    return render_template("recipe.html", recipe=recipe, comments=comments, ingredients = ingredients)

 

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
    nr_of_recipes = ""
    for a in amount:
         nr_of_recipes = a
    random_numbers = []
    for i in range(int(number)):
        random_numbers.append(randint(0, nr_of_recipes))
    while int(number)>len(recipe_list):
        for i in random_numbers:
            db.cursor.execute(psql,(i,))
            for recipe in db.cursor:
                recipe_list.append(list(recipe))
    return redirect(url_for("matsedel", recipe_list = recipe_list))

@app.route('/matsedel/')
def matsedel():
    return render_template("matsedel.html", recipe_list = request.args.getlist("recipe_list"))


@app.route('/add_comment/', methods=['POST'])
def add_comment():
    recipe_id = request.form["recipe_ID"]
    username = session["user_email"]
    comment = request.form["comment"]
    now = datetime.now()
    time_published = now.strftime("%Y-%m-%d %H:%M")

    
    sql = "INSERT INTO comment VALUES (DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (recipe_id, username, comment, time_published))
    db.conn.commit()

    return redirect("/recipe/{}/".format(recipe_id))

UPLOAD_FOLDER = "food4thought_app/static/images/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_profile_image/', methods=['POST'])
def upload_profile_image():

    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            flash("Profilbild uppladdad!")
            sql = "update users set image_url = %s where email = %s"
            db.cursor.execute(sql, (image.filename, session["user_email"]))
            db.conn.commit()
            session["profile_pic"] = image.filename
            return redirect(url_for("profile"))

    return render_template(url_for("profile"))

@app.route('/mina-recept/')
def my_recipes():
    recipe_list = []
    sql = "select username, title, recipe_description, instructions, time_published, recipe_ID, image_url from recipe where username = %s"

    db.cursor.execute(sql,(session["user_email"],))

    for recipe in db.cursor:
        recipe_list.append(recipe) 

    return render_template("myrecipes.html", recipe_list = recipe_list)
