from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import (current_user, confirm_login, login_required,
                             login_fresh)

from app import db
from app.decorators import admin_required
from app.forms.users import LoginForm
from app.forms.pages import PageForm
from app.models.blog import Post, Comment
from app.models.users import User
from app.models.pages import Page
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
    info = [get_python_version(), get_flask_version(), get_app_version(),
               Post.query.count(), Comment.query.count(), User.query.count()]
    return render_template("admin/overview.html", info=info)


@mod.route("/manage_posts")
@admin_required
def manage_posts():
    posts = Post.query.order_by(Post.pid.desc())
    return render_template("admin/manage_posts.html", posts=posts)


@mod.route("/manage_pages")
@admin_required
def manage_pages():
    pages = Page.query.all()
    return render_template("admin/manage_pages.html", pages=pages)


@mod.route("/manage_users")
@admin_required
def manage_users():
    users = User.query.all()
    return render_template("admin/manage_users.html", users=users)


@admin_required
@mod.route("/user/<username>/delete")
def delete_user(username):
    if current_user.username == username:
        flash("You cannot delete yourself", "error")
    else:
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()


@admin_required
@mod.route("/page/new", methods=["GET", "POST"])
def new_page():
    form = PageForm(request.form)

    if form.validate_on_submit():
        page = Page(title=form.title.data, content=form.content.data,
                    category=form.category.data, user_id=current_user.uid)

        db.session.add(page)
        db.session.commit()

        flash("Your Page has been submitted!", "success")

    return render_template("admin/new_page.html", form=form)


@admin_required
@mod.route("/page/<category>/edit", methods=["GET", "POST"])
def edit_page(category):
    page = Page.query.filter_by(category=category).first()

    form = PageForm(request.form)

    if form.validate_on_submit():
        page.title = form.title.data
        page.content = form.content.data
        page.category = form.category.data

        db.session.add(page)
        db.session.commit()

        flash("Your changes have been saved. Redirecting...", "success")
        return redirect(url_for("admin.manage_pages"))
    else:
        form.title.data = page.title
        form.content.data = page.content
        form.category.data = page.category

    return render_template("admin/edit_page.html", page=page, form=form)


@admin_required
@mod.route("/page/<category>/delete")
def delete_page(category):
    page = Page.query.filter_by(category=category).first()

    if page:
        db.session.delete(page)
        db.session.commit()

        flash("Your page has been deleted.", "success")
        return redirect(url_for("admin.manage_pages"))
    else:
        flash("I have no page in my database that is named like this.", "error")
        return redirect(url_for("admin.manage_pages"))
