from flask import render_template, request, abort
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from app.costcenter.models import CostCenter
from app import app, db

CostCenterForm = model_form(CostCenter, FlaskForm)


@app.route("/costcenter/")
def costcenter_add_new_form():
    form = CostCenterForm(request.form)

    return _render_costcenter_form(form)


@app.route("/costcenter/", methods=["POST"])
def costcenter_perform_add():
    model = CostCenter()

    form = CostCenterForm(request.form, model)

    if _validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>')
def costcenter_edit_existing_form(id=None):
    model = _get_costcenter_model(id)
    form = CostCenterForm(request.form, model)

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>', methods=["POST"])
def costcenter_perform_update(id=None):
    model = _get_costcenter_model(id)
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
    return render_template("costcenter/costcenter-form.html", form=form)


def _get_costcenter_model(id):
    model = CostCenter.query.get(id)
    
    if not model:
        abort(404)

    return model