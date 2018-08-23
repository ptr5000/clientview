from flask import render_template, request, redirect, url_for
from flask_login import current_user
from app.subcontractor.models import Subcontractor
from app.subcontractor.forms import SubcontractorForm
from app.auth.decorators import login_required
from app.auth.models import Roles
from app import app, db
from app.utils import validate_and_populate_form_model

@app.route('/subcontractor/')
@login_required(Roles.DEFAULT)
def subcontractor_add_details_form():
    model, _ = _get_or_create_subcontractor_model()
    form = SubcontractorForm(request.form, model)
    return _render_subcontractor_form(form)


@app.route('/subcontractor/<id>/')
@login_required(Roles.ADMIN)
def subcontractor_get_details(id=None):
    details = Subcontractor.get_details(id)
    return render_template("subcontractor/subcon-details.html", details=details)


@app.route("/subcontractor/", methods=["POST"])
@login_required(Roles.DEFAULT)
def subcontractor_save_details_form():
    model, created = _get_or_create_subcontractor_model()

    form = SubcontractorForm(request.form, model)

    if validate_and_populate_form_model(form, model):
        if created:
            db.session().add(model)
        db.session().commit()
        return redirect(url_for("subcontractor_add_details_form"))

    return _render_subcontractor_form(form)


def _get_or_create_subcontractor_model():
    model = Subcontractor.query.filter_by(user_id=current_user.get_id()).first()

    if not model:
        model = Subcontractor(user_id=current_user.get_id())
        return model, True

    return model, False


def _render_subcontractor_form(form):
    return render_template("subcontractor/subcon-edit.html", form=form)
