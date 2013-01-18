from flask import Blueprint, request, render_template, flash, g, redirect, url_for
from flask.ext.login import current_user, login_required

from datetime import datetime

from app import app, db, lm
from app.forms.users import ProfileForm
from app.models.users import User

mod = Blueprint('users', __name__, url_prefix='/user')


@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.lastvisit = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@mod.route("/")
def users():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for("users.profile", username=current_user))
    return redirect(url_for("frontend.login"))

@mod.route("/<username>")
def profile(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash("User " + username + " not found", "info")
        return redirect(url_for("frontend.index"))
    return render_template("users/profile.html",
        user = user)

@mod.route("/<username>/edit", methods=["GET", "POST"])
@login_required
def editprofile(username):
    if username == g.user.username:
        user = User.query.filter_by(username = username).first()
        form = ProfileForm()
        if form.validate_on_submit():
            user.fullname = form.fullname.data
            user.location = form.location.data
            user.sex = form.sex.data
            user.about_me = form.about_me.data

            db.session.add(user)
            db.session.commit()

            flash("Your changes have been saved", "success")
            return redirect(url_for("users.profile", username=user))
        else:
            form.fullname.data = g.user.fullname
            form.location.data = g.user.location
            form.sex.data = g.user.sex
            form.about_me.data = g.user.about_me
    else:
        return redirect(url_for("frontend.index"))
    return render_template('users/editprofile.html',
        user = user,
        form = form)
