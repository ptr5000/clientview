from flask import render_template, request, abort, redirect, url_for
from app.order.models import ProductOrder, Order
from app import app, db
from app.utils import validate_and_populate_form_model
from app.order.forms import OrderForm
from app.auth.decorators import login_required
from app.auth.models import Roles

@app.route("/order/")
@login_required(Roles.ADMIN)
def order_browser():
    form = OrderForm(request.form)

    orders = ProductOrder.query.paginate(max_per_page=5)

    return render_template("order/order-browser.html",
                           form=form, orders=orders)



@app.route("/order/", methods=["POST"])
@login_required(Roles.ADMIN)
def order_perform_add():
    form = OrderForm(request.form)
 
    if form.validate():
        order_id = _add_order_to_db(form)
        _add_product_order_to_db(form, order_id)
        return redirect(url_for("order_browser"))

    return _render_order_form(form)


@app.route('/order/<id>')
@login_required(Roles.ADMIN)
def order_edit_existing_form(id=None):
    model = _get_order_model_or_abort(id)
    form = OrderForm(request.form, model)

    return _render_order_form(form)


@app.route('/order/<id>/delete')
@login_required(Roles.ADMIN)
def order_perform_delete(id=None):
    model = _get_order_model_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("order_browser"))


@app.route('/order/<id>', methods=["POST"])
@login_required(Roles.ADMIN)
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

def _add_order_to_db(form):
    order = Order()
    order.status = 1
    order.subcontractor_id = form.subcontractor.data
    order.cost_center_id = form.cost_center.data
    db.session().add(order)
    db.session().flush()
    return order.id

def _add_product_order_to_db(form, order_id):
    po = ProductOrder()
    po.order_id = order_id
    po.product_id = form.product.data
    db.session().add(po)
    db.session().commit()
