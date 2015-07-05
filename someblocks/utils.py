import feedparser
import mcstatus
import ts3

from flask import current_app

from someblocks.extensions import cache


@cache.cached(timeout=180, key_prefix="ts3_stats")
def get_teamspeak_stats():
    stats = None
    try:
        server = ts3.TS3Server(
            ip=current_app.config["TS3_IP"],
            port=current_app.config["TS3_PORT"],
            id=current_app.config["TS3_VIRTUALSERVER_ID"]
        )
        server.login(
            current_app.config["TS3_QUERYUSER"],
            current_app.config["TS3_QUERYPASSWORD"]
        )
        stats = {"clients": server.clientlist(),
                 "server": server.serverlist().data}
    except:
        stats = None
    return stats


def get_minecraft_stats():
    try:
        server = mcstatus.MinecraftServer(
            host=current_app.config["MC_SERVER"],
            port=current_app.config["MC_PORT"]
        )

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
