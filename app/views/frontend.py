from flask import Blueprint, render_template
from flask.ext.login import current_user

from app.helpers import get_minecraft_stats, get_rss_feed

from app.models.pages import Page

mod = Blueprint("frontend", __name__)


@mod.route("/")
def index():
    full_stats = get_minecraft_stats()
    rss = get_rss_feed()

    return render_template("frontend/index.html",
                           user=current_user,
                           rss=rss,
                           hostname="someblocks.com",
                           hostip=full_stats["hostip"],
                           players=full_stats["players"],
                           online=full_stats["numplayers"],
                           maxplayers=full_stats["maxplayers"])


@mod.route("/<category>")
def pages(category):
    page = Page.query.filter_by(category=category).first()
    return render_template("pages/pages.html", page=page)