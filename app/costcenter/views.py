from flask import render_template, request, abort, redirect, url_for
from flask_login import login_required
from app.costcenter.models import CostCenter
from app.costcenter.forms import CostCenterForm
from app import app, db
from app.utils import validate_and_populate_form_model


@app.route("/costcenter/")
@login_required
def costcenter_browser():
    form = CostCenterForm(request.form)

    cost_centers = CostCenter.query.paginate(max_per_page=5)

    return render_template("costcenter/costcenter-browser.html",
                           form=form, cost_centers=cost_centers)


@app.route("/costcenter/", methods=["POST"])
@login_required
def costcenter_perform_add():
    model = CostCenter()

    form = CostCenterForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("costcenter_browser"))

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>')
@login_required
def costcenter_edit_existing_form(id=None):
    model = _get_costcenter_model_or_abort(id)
    form = CostCenterForm(request.form, model)

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>/delete')
@login_required
def costcenter_perform_delete(id=None):
    model = _get_costcenter_model_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("costcenter_browser"))


@app.route('/costcenter/<id>', methods=["POST"])
@login_required
def costcenter_perform_update(id=None):
    model = _get_costcenter_model_or_abort(id)
    form = CostCenterForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_costcenter_form(form)


def _render_costcenter_form(form):
    return render_template("costcenter/costcenter-form-standalone.html", form=form)


def _get_costcenter_model_or_abort(id):
    model = CostCenter.query.get(id)

    if not model:
        abort(404)

    return model
