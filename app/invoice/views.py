from flask import render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from app.invoice.models import Invoice
from app.order.models import ProductOrder, Order
from app.subcontractor.models import Subcontractor
from app import app


@app.route("/invoice/")
@login_required
def invoice_browser():
    subcontractor = Subcontractor.query.filter_by(user_id=current_user.get_id()).first()
    orders = _get_orders_with_invoices(subcontractor.id).paginate(max_per_page=5)

    return render_template("invoice/invoice-browser.html", orders=orders)


@app.route('/invoice/<id>/', methods=["GET"])
@login_required
def invoice_view(id=None):
    order = _get_order_or_abort(id)
    invoice = _get_invoice_or_abort(order.id)

    return  _render_invoice(invoice)


@app.route('/invoice/<id>/new', methods=["GET"])
@login_required
def invoice_create_new(id=None):
    model = _get_order_or_abort(id)
    _ = Invoice.create_invoice(model)

    return redirect_to_invoice_view(id)


@app.route('/invoice/<id>/send', methods=["GET"])
@login_required
def invoice_send(id=None):
    model = _get_order_or_abort(id)
    invoice = _get_invoice_or_abort(model.id)
    invoice.send()

    return redirect_to_invoice_view(id)


def _get_order_or_abort(id):
    model = Order.query.get(id)

    if not model:
        abort(404)

    return model


def _get_invoice_or_abort(order_id):
    invoice = Invoice.query.filter_by(order_id=order_id).first()

    if not invoice:
        abort(404)

    return invoice


def _get_orders_with_invoices(subcontractor_id):
    return (Order.query
            .join(ProductOrder)
            .outerjoin((Invoice, Invoice.order_id == Order.id))
            .filter(Order.subcontractor_id == subcontractor_id))


def _render_invoice(invoice):
    products = ProductOrder.query.filter_by(order_id=invoice.order_id)
    return render_template("invoice/invoice.html", 
                           invoice=invoice, 
                           products=products)


def redirect_to_invoice_view(id):
    return redirect(url_for("invoice_view", id=id))
