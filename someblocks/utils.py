import random
import sys
import feedparser

from flask import current_app, __version__ as flask_version

from .extensions import cache
from .libs.mcstatus.minecraft_query import MinecraftQuery


@cache.cached(timeout=60, key_prefix="minecraft_stats")
def get_minecraft_stats():
    try:
        query = MinecraftQuery(current_app.config["MC_SERVER"],
                               current_app.config["MC_PORT"], 1, 1)
        stats = query.get_rules()
    except:
        stats = {"hostip": None, "players": None, "numplayers": None,
                 "maxplayers": None}
    return stats


@cache.cached(timeout=300, key_prefix="rss_feed")
def get_rss_feed():
    try:
        d = feedparser.parse(current_app.config["RSS_MCUPDATES"])
        rss = [[d.entries[i].title, d.entries[i].link] for i in range(5)]
    except:
        rss = None
    return rss


def format_date(value, dateformat='normal'):
    if dateformat == 'normal':
        dateformat = '%d.%m.%Y @ %H:%M'
    elif dateformat == 'alphabet':
        dateformat = '%b %d %Y'
    return value.strftime(dateformat)


def generate_random_pass(length=8):
    return "".join(chr(random.randint(33, 126)) for i in range(length))


def get_python_version():
    return "%s.%s" % (sys.version_info[0], sys.version_info[1])


def get_flask_version():
    return flask_version


def get_app_version():
    return "0.2"  # need to change that
