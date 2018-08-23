from functools import reduce
from flask import render_template, request, abort, redirect, url_for
from app.order.models import ProductOrder, Order
from app.product.models import Product
from app import app, db
from app.utils import validate_and_populate_form_model
from app.order.forms import OrderForm
from app.auth.decorators import login_required
from app.auth.models import Roles

@app.route("/order/")
@login_required(Roles.ADMIN)
def order_browser():
    form = OrderForm(request.form)

    orders = Order.query.paginate(max_per_page=5)

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
def order_details(id=None):
    order = _get_order_or_abort(id)

    products, total_sum = _get_product_orders_and_their_total_sum(order.id)

    return render_template("order/order-details.html", 
                           order=order, 
                           products=products,
                           total_sum=total_sum)


@app.route('/order/<id>/edit')
@login_required(Roles.ADMIN)
def order_edit_existing_form(id=None):
    model = _get_order_or_abort(id)
    form = OrderForm(request.form, model)

    return _render_order_form(form)


@app.route('/order/<id>/delete')
@login_required(Roles.ADMIN)
def order_perform_delete(id=None):
    model = _get_order_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("order_browser"))


@app.route('/order/<id>', methods=["POST"])
@login_required(Roles.ADMIN)
def order_perform_update(id=None):
    model = _get_order_or_abort(id)
    form = OrderForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_order_form(form)


def _render_order_form(form):
    return render_template("order/order-form-standalone.html", form=form)


def _get_order_or_abort(id):
    order = Order.query.get(id)

    if not order:
        abort(404)

    return order

def _add_order_to_db(form):
    order = Order()
    order.status = 1
    order.subcontractor_id = form.subcontractor.data
    order.cost_center_id = form.cost_center.data
    db.session().add(order)
    db.session().flush()
    return order.id

def _get_selected_products(form):
    products = [form.product1.data,
                form.product2.data,
                form.product3.data]

    return filter(lambda s: s != -1, products)

def _add_product_order_to_db(form, order_id):
    products = _get_selected_products(form)

    for product in products:
        po = ProductOrder()
        po.order_id = order_id
        po.product_id = product
        db.session().add(po)

    db.session().commit()

def _get_product_orders_and_their_total_sum(order_id):
    products = ProductOrder.query.filter_by(order_id=order_id)
    total_sum = reduce(lambda sum, po: sum+po.product.price, products, 0)
    return products, total_sum
