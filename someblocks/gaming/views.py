from flask import Blueprint, render_template, redirect, current_app

from someblocks.utils import get_minecraft_stats, get_rss_feed, \
    get_teamspeak_stats

gaming = Blueprint("gaming", __name__)


DOWNLOAD_URI = "/downloads"
PREVIEW_URI = "/map"

OLD_WORLDS = (
    {"name": "First World",
     "download_uri": "%s/first_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/88/64/-87/-6/1/0" % PREVIEW_URI,
     "size": "32MB",
     "gamemode": "survival"
     },
    {"name": "Second World",
     "download_uri": "%s/second_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/76/64/15/-6/2/0" % PREVIEW_URI,
     "size": "61MB",
     "gamemode": "survival"
     },
    {"name": "Third World",
     "download_uri": "%s/third_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": None,
     "size": "25MB",
     "gamemode": "survival"
     },
    {"name": "Third World",
     "download_uri": "%s/third_world_c.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/64/64/-152/-6/3/0" % PREVIEW_URI,
     "size": "46MB",
     "gamemode": "creative"
     },
    {"name": "Fourth World",
     "download_uri": "%s/fourth_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/-238/64/291/-6/4/0" % PREVIEW_URI,
     "size": "36MB",
     "gamemode": "survival"
     },
    {"name": "Fifth World",
     "download_uri": "%s/fifth_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/-30/64/223/-6/5/0" % PREVIEW_URI,
     "size": "16MB",
     "gamemode": "survival"
     },
    {"name": "Sixth World",
     "download_uri": "%s/sixth_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/26/64/82/-6/6/0" % PREVIEW_URI,
     "size": "35MB",
     "gamemode": "survival"
     },
    {"name": "Seventh World",
     "download_uri": "%s/seventh_world_c.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/471/64/393/-6/7/0" % PREVIEW_URI,
     "size": "20MB",
     "gamemode": "creative"
     },
    {"name": "Eigth World",
     "download_uri": "%s/eigth_world_s.tar.gz" % DOWNLOAD_URI,
     "preview_uri": "%s/#/79/64/304/-7/8/0" % PREVIEW_URI,
     "size": "43MB",
     "gamemode": "survival"
     },
)


@gaming.route("/")
def index():
    mc = get_minecraft_stats()
    rss = get_rss_feed()
    ts3 = get_teamspeak_stats()
    return render_template("gaming/index.html", rss=rss, mc=mc, ts3=ts3)


@gaming.route("/server")
def server():
    return render_template("gaming/server.html", old_worlds=OLD_WORLDS)


@gaming.route("/map")
def map():
    # redirect to the minecraft live map url
    return redirect(current_app.config["MINECRAFT_LIVEMAP_URL"], code=302)
