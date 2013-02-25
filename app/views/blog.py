from datetime import datetime

from sqlalchemy import func
from flask import Blueprint, render_template, redirect, flash, url_for
from flask.ext.login import login_required, current_user

from app import db
from app.models.blog import Post, Comment
from app.forms.blog import PostForm, CommentForm


mod = Blueprint("blog", __name__, url_prefix="/news")


@mod.route("/", methods=["GET"])
def news():
    #posts = Post.query.order_by(Post.pid.desc())
    #return render_template("blog/news.html", posts=posts)
    posts_and_comments = db.session.query(Post, func.count(Post.comments)).all()
    return render_template("blog/news.html", posts_and_comments=posts_and_comments)


@mod.route("/post/<id>", methods=["GET"])
def post(id):
    form = CommentForm()

    post = Post.query.filter_by(pid=id).first()
    comment = Comment.query.filter_by(post_id=id).all()
    return render_template("blog/post.html", post=post, id=post.pid, form=form,
                            comments=comment)


@mod.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if current_user.can_compose_post():
        if form.validate_on_submit():
            post = Post(
                title=form.title.data, body=form.body.data,
                    date_created=datetime.utcnow(), user_id=current_user.uid)

            db.session.add(post)
            db.session.commit()
            flash("Your post has been submitted!", "success")
            return redirect(url_for("blog.news"))
    else:
        flash("You are not allowed to compose a post", "error")
        return redirect(url_for("blog.news"))
    return render_template("blog/new_post.html", form=form)


@mod.route("/post/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(id):
    form = PostForm()
    if current_user.can_edit_post(post_id=id) or current_user.is_admin():
        post = Post.query.filter_by(pid=id).first()

        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data

            db.session.add(post)
            db.session.commit()

            flash("Your changes have been saved", "success")
            return redirect(url_for("blog.news"))

        else:
            form.title.data = post.title
            form.body.data = post.body
    else:
        flash("You are not allowed to edit this post", "error")
        return redirect(url_for("blog.news"))

    return render_template("blog/edit_post.html", form=form, id=post.pid)


@mod.route("/post/<id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(id):
    if current_user.can_edit_post(post_id=id) or current_user.is_admin():
        post = Post.query.filter_by(pid=id).first()

        db.session.delete(post)
        db.session.commit()

        flash("Your post has been deleted", "success")
        return redirect(url_for("blog.news"))
    else:
        flash("You cannot delete someone else's post", "error")
        return redirect(url_for("blog.news"))

    return render_template("blog/post.html", post=post, pid=id)


@mod.route("/post/<id>/comment", methods=["GET", "POST"])
@login_required
def new_comment(id):
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(user_id=current_user.uid,
                          date_created=datetime.utcnow(),
                          content=form.content.data, post_id=id)

        db.session.add(comment)
        db.session.commit()

    return redirect(url_for("blog.post", id=id))
