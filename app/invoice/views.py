from flask import render_template, abort
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


@app.route('/invoice/<id>/new', methods=["GET"])
@login_required
def invoice_create_new(id=None):
    model = _get_product_order_or_abort(id)

    invoice = Invoice.create_invoice_from_product_order(model)

    return render_template("invoice/invoice.html",
                           invoice=invoice)


def _get_product_order_or_abort(id):
    model = ProductOrder.query.get(id)

    if not model:
        abort(404)

    return model


def _get_orders_with_invoices(subcontractor_id):
    return (ProductOrder.query
            .join(Order)
            .outerjoin((Invoice, Invoice.product_order_id == ProductOrder.id))
            .filter(Order.subcontractor_id == subcontractor_id))