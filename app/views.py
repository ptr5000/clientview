# pylint: disable=W0611
from flask import render_template
from flask_login import login_required

import app.auth.views
import app.costcenter.views

from . import app


@app.route("/")
@login_required
def index():
    return render_template("index.html")
