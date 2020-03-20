from flask import render_template
from food4thought_app import app


@app.route('/')
def index():
    return render_template("index.html")