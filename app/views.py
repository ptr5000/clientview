# pylint: disable=W0611
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

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
    if current_user.is_admin():
        return redirect(url_for("invoice_inbox"))
    else:
        return redirect(url_for("invoice_browser"))
