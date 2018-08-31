from flask import render_template, request, abort, redirect, url_for
from app.auth.decorators import login_required
from app.auth.models import Roles
from app.costcenter.models import CostCenter
from app.costcenter.forms import CostCenterForm
from app import app, db
from app.utils import validate_and_populate_form_model, render_default_row_view


@app.route("/costcenter/")
@login_required(Roles.ADMIN)
def costcenter_browser():
    form = CostCenterForm(request.form)

    cost_centers = CostCenter.query.order_by(CostCenter.id.desc()).paginate(max_per_page=5)

    return render_template("costcenter/costcenter-browser.html",
                           form=form, cost_centers=cost_centers)


@app.route("/costcenter/", methods=["POST"])
@login_required(Roles.ADMIN)
def costcenter_perform_add():
    model = CostCenter()

    form = CostCenterForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().add(model)
        db.session().commit()
        return redirect(url_for("costcenter_browser"))

    return _render_costcenter_form(form)


@app.route('/costcenter/<id>')
@login_required(Roles.ADMIN)
def costcenter_view(id=None):
    return render_default_row_view(_create_cost_center_form_from_existing_data(id))


@app.route('/costcenter/<id>/edit')
@login_required(Roles.ADMIN)
def costcenter_edit_existing_form(id=None):
    return _render_costcenter_form(_create_cost_center_form_from_existing_data(id))


@app.route('/costcenter/<id>/delete')
@login_required(Roles.ADMIN)
def costcenter_perform_delete(id=None):
    model = _get_costcenter_or_abort(id)
    db.session().delete(model)
    db.session().commit()
    return redirect(url_for("costcenter_browser"))


@app.route('/costcenter/<id>/edit', methods=["POST"])
@login_required(Roles.ADMIN)
def costcenter_perform_update(id=None):
    model = _get_costcenter_or_abort(id)
    form = CostCenterForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        db.session().commit()

    return _render_costcenter_form(form)


def _render_costcenter_form(form):
    return render_template("costcenter/costcenter-form-standalone.html", form=form)


def _get_costcenter_or_abort(id):
    model = CostCenter.query.get(id)

    if not model:
        abort(404)

    return model


def _create_cost_center_form_from_existing_data(id):
    model = _get_costcenter_or_abort(id)
    form = CostCenterForm(request.form, model)
    return form
