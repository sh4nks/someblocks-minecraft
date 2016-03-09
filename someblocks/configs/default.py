import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Indicates that it is a dev environment
DEBUG = True
SECRET_KEY = "SecretKeyForSessionSigning"

# Caching
CACHE_TYPE = "simple"

# App specific configurations
# RSS
RSS_MCUPDATES = "http://mcupdate.tumblr.com/rss"

# Minecraft Query
MC_SERVER = "someblocks.com"
MC_PORT = 25565
MC_LIVE_MAP_URL = "gaming.someblocks.com/map"

# Teamspeak 3 Query
TS3_IP = "someblocks.com"
TS3_PORT = 10011
TS3_VIRTUALSERVER_ID = 1
TS3_QUERYUSER = "serveradmin"
TS3_QUERYPASSWORD = "supersecretpassword"

# Routing
MAIN_URL = ""
GAMING_URL = "/gaming"
GAMING_SUBDOMAIN = ""
