from flask import render_template, request, abort, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms.ext.sqlalchemy.orm import model_form
from app.product.models import Product
from app import app, db
from app.utils import validate_and_populate_form_model

ProductForm = model_form(Product, FlaskForm)

@app.route("/product/")
@login_required
def product_browser():
    form = ProductForm(request.form)

    products = Product.query.paginate(max_per_page=5)

    return render_template("product/product-browser.html",
                           form=form, products=products)



@app.route("/product/", methods=["POST"])
@login_required
def product_perform_add():
    model = Product()

    form = ProductForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("product_browser"))

    return _render_product_form(form)


@app.route('/product/<id>')
@login_required
def product_edit_existing_form(id=None):
    model = _get_product_model_or_abort(id)
    form = ProductForm(request.form, model)

    return _render_product_form(form)


@app.route('/product/<id>/delete')
@login_required
def product_perform_delete(id=None):
    model = _get_product_model_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("product_browser"))


@app.route('/product/<id>', methods=["POST"])
@login_required
def product_perform_update(id=None):
    model = _get_product_model_or_abort(id)
    form = ProductForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_product_form(form)


def _render_product_form(form):
    return render_template("product/product-form-standalone.html", form=form)


def _get_product_model_or_abort(id):
    model = Product.query.get(id)

    if not model:
        abort(404)

    return model