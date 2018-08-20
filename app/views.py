# pylint: disable=W0611
from flask import render_template
from flask_login import login_required

import app.auth.views
import app.costcenter.views
import app.subcontractor.views
import app.order.views
import app.product.views
import app.invoice.views

from . import app

@app.route("/")
@login_required
def index():
    return render_template("index.html")
