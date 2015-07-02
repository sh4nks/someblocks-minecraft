from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/about")
def about():
    return render_template("main/about.html")


@main.route("/projects")
def projects():
    return render_template("main/projects.html")
