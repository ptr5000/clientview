from flask import render_template, request, abort, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms.ext.sqlalchemy.orm import model_form
from app.order.models import Order
from app import app, db
from app.utils import validate_and_populate_form_model

OrderForm = model_form(Order, FlaskForm)

@app.route("/order/")
@login_required
def order_browser():
    form = OrderForm(request.form)

    orders = Order.query.paginate(max_per_page=5)

    return render_template("order/order-browser.html",
                           form=form, orders=orders)



@app.route("/order/", methods=["POST"])
@login_required
def order_perform_add():
    model = Order()

    form = OrderForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("order_browser"))

    return _render_order_form(form)


@app.route('/order/<id>')
@login_required
def order_edit_existing_form(id=None):
    model = _get_order_model_or_abort(id)
    form = OrderForm(request.form, model)

    return _render_order_form(form)


@app.route('/order/<id>/delete')
@login_required
def order_perform_delete(id=None):
    model = _get_order_model_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("order_browser"))


@app.route('/order/<id>', methods=["POST"])
@login_required
def order_perform_update(id=None):
    model = _get_order_model_or_abort(id)
    form = OrderForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_order_form(form)


def _render_order_form(form):
    return render_template("order/order-form-standalone.html", form=form)


def _get_order_model_or_abort(id):
    model = Order.query.get(id)

    if not model:
        abort(404)

    return model
