from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import (current_user, confirm_login, login_required,
                             login_fresh)

from app.decorators import admin_required
from app.forms.users import LoginForm
from app.models.blog import Post, Comment
from app.models.users import User
from app.helpers import get_python_version, get_flask_version, get_app_version

mod = Blueprint("admin", __name__, url_prefix="/admin")


@mod.route("/", methods=["GET", "POST"])
@login_required
def login():
    """
    Reauthenticates a user
    """
    if not current_user.is_admin():
        flash("You don't have the permissions to access this page", "error")
        return redirect(url_for("frontend.index"))

    if not login_fresh():
        form = LoginForm(request.form)
        if form.validate_on_submit():
            confirm_login()
            flash("Reauthenticated")
            return redirect(url_for("admin.overview"))
        return render_template("auth/login.html", form=form)
    return redirect(url_for("admin.overview"))


@mod.route("/overview")
@admin_required
def overview():
    version = [get_python_version(), get_flask_version(), get_app_version(),
               Post.query.count(), Comment.query.count(), User.query.count()]
    return render_template("admin/overview.html", version=version)


@mod.route("/manage_posts")
@admin_required
def manage_posts():
    posts = Post.query.order_by(Post.pid.desc())
    return render_template("admin/manage_posts.html", posts=posts)


@mod.route("/manage_users")
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", users=users)


@admin_required
@mod.route("/user/<username>/delete")
def delete_user(username):
    if current_user.username == username:
        flash("You cannot delete yourself")
    else:
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()
