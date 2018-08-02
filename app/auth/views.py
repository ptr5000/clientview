from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/login")
def auth_login_form():
    return _render_login_form(form=LoginForm(), 
                              registration_form=RegistrationForm())


@app.route("/auth/login", methods=["POST"])
def auth_handle_login():
    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, 
                                password=form.password.data).first()

    if not user:
        return _render_login_form(form=form, 
                                  registration_form=RegistrationForm(), 
                                  error="Invalid credientals")

    login_user(user)

    return redirect(url_for("index"))


@app.route("/auth/register", methods=["POST"])
def auth_handle_registration():
    form = RegistrationForm(request.form)

    if form.validate():
        print("Form validated")
        user = User(form.username.data, form.password.data)
        db.session().add(user)
        db.session().commit()
        login_user(user)
    else:
        print("Got an error")
        return _render_login_form(form=LoginForm(),
                                  registration_form=form)

    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_handle_logout():
    logout_user()
    return redirect(url_for("index"))

def _render_login_form(form, registration_form, error=None):
    return render_template("auth/auth-forms.html", form=form,
                           reg_form=registration_form,
                           error=error)
