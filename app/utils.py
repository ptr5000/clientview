from flask import render_template
from flask_login import current_user

def add_current_user_id_to_model(model):
    if hasattr(model, "user_id"):
        model.user_id = current_user.get_id()


def validate_and_populate_form_model(form, model):
    if form.validate():
        add_current_user_id_to_model(model)
        form.populate_obj(model)
        return True

    return False

def render_default_row_view(form):
    return render_template("default-row-view.html", form=form)
