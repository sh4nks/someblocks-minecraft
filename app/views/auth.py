from datetime import datetime

from werkzeug import check_password_hash, generate_password_hash
from flask import (Blueprint, request, render_template, flash, redirect,
                   url_for)

from flask.ext.login import (login_user, logout_user, current_user,
                             confirm_login, login_required, login_fresh)

from app import app, db, lm
from app.forms.users import RegisterForm, LoginForm, ResetPasswordForm
from app.models.users import User
from app.utils import generate_random_pass
from app.emails import send_new_password


# No url prefix
mod = Blueprint("auth", __name__)


@lm.user_loader
def load_user(uid):
    """
    This is required by the Flask-Login extension
    """
    return User.query.get(int(uid))


@app.before_request
def before_request():
    """
    Updates `lastvisit` before every reguest if the user is authenticated
    """
    if current_user.is_authenticated():
        current_user.lastvisit = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()


@mod.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """

    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("frontend.index"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or
                url_for("frontend.index"))

        flash("Wrong username or password", "error")
    return render_template("auth/login.html", form=form)


@mod.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    """
    Reauthenticates a user
    """
    if not login_fresh():
        flash("For security reasons, you need to refresh your login")
        form = LoginForm(request.form)
        if form.validate_on_submit():
            confirm_login()
            flash("Reauthenticated")
            return redirect(request.args.get("next") or
                url_for("frontend.index"))
        return render_template("auth/login.html", form=form)
    return redirect(request.args.get("next") or url_for("frontend.index"))


@mod.route("/logout")
def logout():
    """
    Logs the user out
    """
    logout_user()
    flash("You were logged out", "info")
    return redirect(url_for("frontend.index"))


@mod.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user
    """

    # Temporary: on my server I"ve disabled the registration
    if not app.config["REGISTRATION"]:
        flash("Registration is currently disabled", "info")
        return redirect(url_for("frontend.index"))

    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("frontend.index"))

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    regdate=datetime.utcnow())
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        flash("Thanks for registering")
        return redirect(url_for("users.profile",
            username=current_user.username))
    return render_template("auth/register.html", form=form)


@mod.route("/resetpassword", methods=["GET", "POST"])
def reset_password():
    """
    Resets the password from a user
    """

    if not app.config["REGISTRATION"]:
        flash("Password resetting via email is currently disabled", "info")
        return redirect(url_for("frontend.index"))

    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        user1 = User.query.filter_by(email=form.email.data).first()
        user2 = User.query.filter_by(username=form.username.data).first()

        if user1.email == user2.email:
            password = generate_random_pass()
            user1.password = generate_password_hash(password)
            db.session.commit()

            send_new_password(user1, password)

            flash("E-Mail sent! Please check your inbox.", "info")
            return redirect(url_for("frontend.login"))
        else:
            flash("You have entered an username or email that is not linked \
                with your account")

    return render_template("auth/reset_password.html", form=form)
