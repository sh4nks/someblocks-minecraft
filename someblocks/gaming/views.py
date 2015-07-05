from flask import Blueprint, render_template, redirect, current_app

from someblocks.utils import get_minecraft_stats, get_rss_feed, \
    get_teamspeak_stats

gaming = Blueprint("gaming", __name__)


@gaming.route("/")
def index():
    mc = get_minecraft_stats()
    rss = get_rss_feed()
    ts3 = get_teamspeak_stats()
    return render_template("gaming/index.html", rss=rss, mc=mc, ts3=ts3)


@gaming.route("/worlds")
def worlds():
    return render_template("gaming/worlds.html")


@gaming.route("/map")
def map():
    # redirect to the minecraft live map url
    return redirect(current_app.config["MINECRAFT_LIVEMAP_URL"], code=302)
