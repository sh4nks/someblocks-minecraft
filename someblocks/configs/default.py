import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Indicates that it is a dev environment
DEBUG = True
SECRET_KEY = "SecretKeyForSessionSigning"

# Caching
CACHE_TYPE = "null"

# App specific configurations
## RSS
RSS_MCUPDATES = "http://mcupdate.tumblr.com/rss"

## Minecraft Query
MC_SERVER = "someblocks.com"
MC_PORT = 25565
MC_LIVE_MAP_URL = ""

MAIN_URL = ""
GAMING_URL = "/gaming"
GAMING_SUBDOMAIN = ""
