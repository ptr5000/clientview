from flask import render_template, request, abort, redirect, url_for
from flask_login import login_required
from app.invoice.models import Invoice
from app.invoice.forms import InvoiceForm
from app import app, db
from app.utils import validate_and_populate_form_model


@app.route("/invoice/")
@login_required
def invoice_browser():
    form = InvoiceForm(request.form)

    invoices = Invoice.query.paginate(max_per_page=5)

    return render_template("invoice/invoice-browser.html",
                           form=form, invoices=invoices)


@app.route("/invoice/", methods=["POST"])
@login_required
def invoice_perform_add():
    model = Invoice()

    form = InvoiceForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("invoice_browser"))

    return _render_invoice_form(form)


@app.route('/invoice/<id>')
@login_required
def invoice_edit_existing_form(id=None):
    model = _get_invoice_model_or_abort(id)
    form = InvoiceForm(request.form, model)

    return _render_invoice_form(form)


@app.route('/invoice/<id>/delete')
@login_required
def invoice_perform_delete(id=None):
    model = _get_invoice_model_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("invoice_browser"))


@app.route('/invoice/<id>', methods=["POST"])
@login_required
def invoice_perform_update(id=None):
    model = _get_invoice_model_or_abort(id)
    form = InvoiceForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_invoice_form(form)


def _render_invoice_form(form):
    return render_template("invoice/invoice-form-standalone.html", form=form)


def _get_invoice_model_or_abort(id):
    model = Invoice.query.get(id)

    if not model:
        abort(404)

    return model
