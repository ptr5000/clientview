from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm

@app.route("/auth/login")
def auth_login_form():
    return _render_forms(form=LoginForm(), 
                         registration_form=RegistrationForm())


@app.route("/auth/login", methods=["POST"])
def auth_handle_login():
    form = LoginForm(request.form)

    if not _login_user(form):
        return _render_forms(form=form, 
                             registration_form=RegistrationForm(), 
                             error="Invalid credentials")
    
    return redirect(url_for("index"))


@app.route("/auth/register", methods=["GET"])
def auth_register():
    return _render_forms(form=LoginForm(),
                         registration_form=RegistrationForm(),
                         active_tab="register")


@app.route("/auth/register", methods=["POST"])
def auth_handle_registration():
    form = RegistrationForm(request.form)

    if not _add_user_to_db(form):
        return _render_forms(form=LoginForm(),
                             registration_form=form,
                             active_tab="register")

    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_handle_logout():
    logout_user()
    return redirect(url_for("index"))


def _add_user_to_db(form):
    if form.validate():
        user = User(form.username.data, form.password.data)
        db.session().add(user)
        db.session().commit()
        login_user(user)
        return True

    return False


def _login_user(form):
    user = User.query.filter_by(username=form.username.data).first()

    if user and user.validate_password(form.password.data):
        login_user(user)
        return True

    return False
    


def _render_forms(form, registration_form, active_tab="login", error=None):
    return render_template("auth/auth-forms.html", form=form,
                           reg_form=registration_form,
                           active_tab=active_tab,
                           error=error)

