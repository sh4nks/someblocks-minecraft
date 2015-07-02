import feedparser
import mcstatus

from flask import current_app

from .extensions import cache


@cache.cached(timeout=60, key_prefix="minecraft_stats")
def get_minecraft_stats():
    try:
        server = mcstatus.MinecraftServer(current_app.config["MC_SERVER"],
                                          current_app.config["MC_PORT"])
        query = server.query()
    except:
        query = None
    return query


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
