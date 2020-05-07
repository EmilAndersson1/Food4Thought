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