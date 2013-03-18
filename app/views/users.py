from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import current_user, login_required

from app import db
from app.forms.users import ProfileForm
from app.models.users import User


mod = Blueprint("users", __name__, url_prefix="/user")


@mod.route("/")
def users():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for("users.profile", username=current_user))
    return redirect(url_for("auth.login"))


@mod.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User " + username + " not found", "info")
        return redirect(url_for("frontend.index"))
    return render_template("users/profile.html", user=user)


@mod.route("/<username>/edit", methods=["GET", "POST"])
@login_required
def editprofile(username):
    user = User.query.filter_by(username=username).first()
    if username == current_user.username:
        form = ProfileForm()
        if form.validate_on_submit():
            user.fullname = form.fullname.data
            user.location = form.location.data
            user.sex = form.sex.data
            user.about_me = form.about_me.data

            db.session.add(user)
            db.session.commit()

            flash("Your changes have been saved", "success")
            return redirect(url_for("users.profile", username=user.username))
        else:
            form.fullname.data = current_user.fullname
            form.location.data = current_user.location
            form.sex.data = current_user.sex
            form.about_me.data = current_user.about_me
    else:
        return redirect(url_for("frontend.index"))
    return render_template("users/editprofile.html", user=user, form=form)
