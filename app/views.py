# pylint: disable=W0611
from flask import render_template
from .costcenter import views
from . import app

@app.route("/")
def index():
    return render_template("index.html")
