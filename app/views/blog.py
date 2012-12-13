from flask import Blueprint, render_template, g, redirect, flash, url_for
from flask.ext.login import login_required

from datetime import datetime

from app import db
from app.models.users import User
from app.models.blog import Post

from app.forms.blog import PostForm, CommentForm

mod = Blueprint('blog', __name__, url_prefix='/news')

@mod.route('/', methods=['GET'])
def news():
    posts = Post.query.order_by(Post.pid.desc())

    return render_template('blog/news.html',
                           title='News',
                           active_blog=True,
                           posts = posts)


@mod.route('/post/<id>', methods=['GET'])
def post(id):
    post = Post.query.filter_by(pid = id).first()
    return render_template('blog/post.html',
                           title = post.title,
                           post = post,
                           active_blog=True,
                           pid = post.pid)


@mod.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, body=form.body.data, \
            date_created=datetime.utcnow(), user_id=g.user.uid)

        db.session.add(post)
        db.session.commit()
        flash("Your post has been submitted!", "success")
        return redirect(url_for("blog.news"))
    return render_template('blog/new_post.html',
                           title = "New Post",
                           form = form,
                           active_blog=True)

@mod.route('/post/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostForm()
    post = Post.query.filter_by(pid = id).first()

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

    return render_template('blog/edit_post.html',
                           title = "Edit Post",
                           form = form,
                           active_blog=True,
                           id = post.pid)
