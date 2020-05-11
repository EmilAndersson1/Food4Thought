from flask import render_template, url_for, request, redirect, session, g
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

    user_email = ""
    if "user_email" in session:
        user_email = session["user_email"]

    return render_template("index.html", recipe_list = recipe_list, user_email = user_email)



@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        #session.pop('user_id', None)
        email = request.form['email']
        user_password = request.form['password']

        sql= "select email, firstname, lastname, user_password from users where email = %s and user_password = %s"
        db.cursor.execute(sql, (email, user_password))
        user = db.cursor.fetchone()

        if user is None:
            return redirect(url_for('login'))

        session["user_email"]=user[0]
        session["user_firstname"]=user[1]
        session["user_lastname"]=user[2]
        return redirect(url_for('index'))

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

    sql= "insert into users(email, firstname, lastname, user_password) values (%s,%s,%s,%s)"

    db.cursor.execute(sql, (email, firstname, lastname, password))
    db.conn.commit()

    return redirect(url_for("index"))


@app.route('/new_recipe/')
def new_recipe():

    return render_template("new_recipe.html")

#tar från formulär för att lägga till recept i databasen
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

    ingredient_name = request.form["ingredient_name1"]
    volume = request.form["volume1"]
    measurement = request.form["measurement1"]

    while True:
        try:
            ingredient_name = request.form["ingredient_name{}".format(x)]
            volume = request.form["volume{}".format(x)]
            measurement = request.form["measurement{}".format(x)]
            sql2 = "INSERT INTO ingredient VALUES (DEFAULT, %s, %s, %s)"
            db.cursor.execute(sql2, (ingredient_name, volume, measurement))
            db.conn.commit()
            x += 1
        except:
            break


    return redirect(url_for("index"))

#tar data från databasen för att skriva ut det på recipe.html
@app.route('/recipe/<recipe_id>/')
def show_recipe(recipe_id):

    recipe = []
    sql = "select recipe_id, username, headline, preamble, instructions, published from recipe where recipe_id = %s"
    db.cursor.execute(sql,(recipe_id,))

    [recipe.append(i) for recipes in db.cursor for i in recipes ]
    """
    comments = []
    sql2 = "select comment.username, comment.comment, comment.curr_time, comment.comment_ID, comment.recipe_ID \
            from comment join recipe \
                on recipe.recipe_ID = comment.recipe_ID \
            where recipe.recipe_ID = %s order by comment.curr_time DESC"    
    db.cursor.execute(sql2,(recipe_ID,))
    for comment in db.cursor:
        comments.append(comment)
    """     
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


"""
@app.route('/add_comment/', methods=['POST'])
def add_comment():
    recipe_ID = request.form["recipe_ID"]
    username = request.form["username"]
    comment = request.form["comment"]
    now = datetime.now()
    time_published = now.strftime("%Y-%m-%d %H:%M")

    
    sql = "INSERT INTO comment VALUES (DEFAULT, %s, %s, %s, %s)"
    db.cursor.execute(sql, (recipe_ID, username, comment, time_published))
    db.conn.commit()

    return redirect("/recipe/{}/".format(recipe_ID))
"""

