from flask import render_template, request, abort, redirect, url_for
from app import app, db
from app.product.models import Product
from app.auth.decorators import login_required
from app.auth.models import Roles
from app.product.forms import ProductForm
from app.utils import validate_and_populate_form_model, render_default_row_view


@app.route("/product/")
@login_required(Roles.ADMIN)
def product_browser():
    form = ProductForm(request.form)

    products = Product.query.order_by(Product.id.desc()).paginate(max_per_page=5)

    return render_template("product/product-browser.html",
                           form=form, products=products)


@app.route("/product/", methods=["POST"])
@login_required(Roles.ADMIN)
def product_perform_add():
    model = Product()

    form = ProductForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("product_browser"))

    return _render_product_form(form)


@app.route('/product/<id>')
@login_required(Roles.ADMIN)
def product_view(id=None):
    return render_default_row_view(_create_product_form(id))

@app.route('/product/<id>/edit')
@login_required(Roles.ADMIN)
def product_edit_existing_form(id=None):
    return _render_product_form(_create_product_form(id))

@app.route('/product/<id>/delete')
@login_required(Roles.ADMIN)
def product_perform_delete(id=None):
    model = _get_product_or_abort(id)
    db.session().delete(model)
    db.session().commit()

    return redirect(url_for("product_browser"))


@app.route('/product/suppliers/<id>', methods=["GET"])
@login_required(Roles.ADMIN)
def product_suppliers(id=None):
    product = _get_product_or_abort(id)

    return render_template("product/suppliers-list.html",
                           product=product, 
                           suppliers=product.get_all_suppliers())


@app.route('/product/<id>/edit', methods=["POST"])
@login_required(Roles.ADMIN)
def product_perform_update(id=None):
    model = _get_product_or_abort(id)
    form = ProductForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_product_form(form)


def _render_product_form(form):
    return render_template("product/product-form-standalone.html", form=form)


def _get_product_or_abort(id):
    model = Product.query.get(id)

    if not model:
        abort(404)

    return model

def _create_product_form(id):
    model = _get_product_or_abort(id)
    form = ProductForm(request.form, model)
    return form
