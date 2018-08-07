
from flask_login import login_required, current_user


def validate_and_populate_form_model(form, model):
    if form.validate():
        if hasattr(model, "user_id"):
            model.user_id = current_user.get_id()
        form.populate_obj(model)
        return True

    return False
