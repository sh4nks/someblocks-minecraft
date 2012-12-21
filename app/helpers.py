import feedparser

from settings import RSS_MCUPDATES
from app import cache
from app.libs.mcstatus.minecraft_query import MinecraftQuery


@cache.cached(timeout=60, key_prefix="minecraft_stats")
def get_minecraft_stats():
    try:
        query = MinecraftQuery("someblocks.com", 25565, 1, 1)
        stats = query.get_rules()
    except:
        stats = {"hostip": None, "players": None, "numplayers": None, "maxplayers": None}
    return stats

@cache.cached(timeout=300, key_prefix="rss_feed")
def get_rss_feed():
    d = feedparser.parse(RSS_MCUPDATES)
    rss = [[d.entries[i].title, d.entries[i].link] for i in range(5)]
    return rss
