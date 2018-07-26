from flask import render_template, request, abort
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from app.costcenter.models import CostCenter
from app import app, db

CostCenterForm = model_form(CostCenter, FlaskForm)

@app.route("/costcenter/")
def costcenter_add_form():
    form = CostCenterForm(request.form)

    return render_template("costcenter/add.html", form=form)

@app.route("/costcenter/", methods=["POST"])
def costcenter_perform_add():
    model = CostCenter()

    form = CostCenterForm(request.form, model)

    if form.validate():
        form.populate_obj(model)
        db.session().add(model)
        db.session().commit()

    return render_template("costcenter/add.html", form=form)

@app.route('/costcenter/<id>')
def costcenter_edit_form(id=None):
    model = CostCenter.query.get(id)
    form = CostCenterForm(request.form, model)
    return render_template("costcenter/add.html", form=form)

@app.route('/costcenter/<id>', methods=["POST"])
def costcenter_perform_update(id=None):
    model = CostCenter.query.get(id)
    form = CostCenterForm(request.form, model)

    if form.validate():
        form.populate_obj(model)
        db.session().commit()

    return render_template("costcenter/add.html", form=form)
