from flask import render_template, abort, redirect, url_for
from flask_login import current_user
from app.auth.decorators import login_required
from app.auth.models import Roles
from app.invoice.models import Invoice, InvoiceStatus
from app.order.models import ProductOrder, Order
from app.subcontractor.models import Subcontractor
from app import app


@app.route("/invoice/inbox/")
@login_required(Roles.ADMIN)
def invoice_inbox():
    invoices = Invoice.query.filter_by(status=InvoiceStatus.sent).order_by(Invoice.sent_date).paginate(max_per_page=5)

    return render_template("invoice/invoice-inbox.html", invoices=invoices)


@app.route("/invoice/")
@login_required(Roles.DEFAULT)
def invoice_browser():
    subcontractor = _get_subcontractor_or_force_to_add_details()

    orders = _get_orders_with_invoices(subcontractor.id).paginate(max_per_page=5)

    return render_template("invoice/invoice-browser.html", orders=orders)

@app.route('/invoice/<id>/', methods=["GET"])
@login_required(Roles.DEFAULT)
def invoice_view(id=None):
    order = _get_order_or_abort(id)
    invoice = _get_invoice_or_abort(order.id)

    return  _render_invoice(invoice)


@app.route('/invoice/<id>/new', methods=["GET"])
@login_required(Roles.DEFAULT)
def invoice_create_new(id=None):
    model = _get_order_or_abort(id)
    _ = Invoice.create_invoice(model)

    return redirect_to_invoice_view(id)


@app.route('/invoice/<id>/send', methods=["GET"])
@login_required(Roles.DEFAULT)
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

def _get_subcontractor_or_force_to_add_details():
    subcontractor = Subcontractor.query.filter_by(user_id=current_user.get_id()).first()

    if subcontractor is None:
        abort(redirect(url_for("subcontractor_add_details_form")))
    
    return subcontractor

def _render_invoice(invoice):
    products = ProductOrder.query.filter_by(order_id=invoice.order_id)
    return render_template("invoice/invoice.html", 
                           invoice=invoice, 
                           products=products)


def redirect_to_invoice_view(id):
    return redirect(url_for("invoice_view", id=id))
