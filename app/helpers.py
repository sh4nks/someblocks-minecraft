import random
import feedparser

from settings import MC_SERVER, MC_PORT, RSS_MCUPDATES
from app import cache
from app.libs.mcstatus.minecraft_query import MinecraftQuery


@cache.cached(timeout=60, key_prefix="minecraft_stats")
def get_minecraft_stats():
    try:
        query = MinecraftQuery(MC_SERVER, MC_PORT, 1, 1)
        stats = query.get_rules()
    except:
        stats = {"hostip": None, "players": None, "numplayers": None,
                 "maxplayers": None}
    return stats


@cache.cached(timeout=300, key_prefix="rss_feed")
def get_rss_feed():
    try:
        d = feedparser.parse(RSS_MCUPDATES)
        rss = [[d.entries[i].title, d.entries[i].link] for i in range(5)]
    except:
        rss = None
    return rss


def generate_random_pass(length=8):
    return "".join(chr(random.randint(33, 126)) for i in range(length))
