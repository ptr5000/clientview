from flask import render_template, request, abort, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from app.costcenter.models import CostCenter
from app import app, db

CostCenterForm = model_form(CostCenter, FlaskForm)

@app.route("/costcenter/")
def costcenter_browser():
    form = CostCenterForm(request.form)

    cost_centers = CostCenter.query.paginate(max_per_page=5)

    return render_template("costcenter/costcenter-browser.html",
                           form=form, cost_centers=cost_centers)



@app.route("/costcenter/", methods=["POST"])
def costcenter_perform_add():
    model = CostCenter()

    form = CostCenterForm(request.form, model)

    if _validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("costcenter_browser"))

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>')
def costcenter_edit_existing_form(id=None):
    model = _get_costcenter_model_or_abort(id)
    form = CostCenterForm(request.form, model)

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>', methods=["POST"])
def costcenter_perform_update(id=None):
    model = _get_costcenter_model_or_abort(id)
    form = CostCenterForm(request.form, model)

    if _validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_costcenter_form(form)


def _validate_and_populate_form_model(form, model):
    if form.validate():
        form.populate_obj(model)
        return True

    return False


def _render_costcenter_form(form):
    return render_template("costcenter/costcenter-form-standalone.html", form=form)


def _get_costcenter_model_or_abort(id):
    model = CostCenter.query.get(id)

    if not model:
        abort(404)

    return model
