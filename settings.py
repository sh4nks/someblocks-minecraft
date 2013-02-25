import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Indicates that it is a dev environment
DEBUG = True
SECRET_KEY = "SecretKeyForSessionSigning"

# SQLAlchemy connection options
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(_basedir, "app.db")

# Protection against form post fraud
CSRF_ENABLED = True
CSRF_SESSION_KEY = "reallyhardtoguess"

# Auth
AUTH_USER_MIXINS = []
AUTH_LOGIN_VIEW = "auth.login"

# Caching
CACHE_TYPE = "simple"

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = "6LfUZ9YSAAAAANtDdyew22z2lnjz-K0Dx8M-gkey"
RECAPTCHA_PRIVATE_KEY = "6LfUZ9YSAAAAAHgDBflMFQTVdlTA3__yYx8CBGII"
RECAPTCHA_OPTIONS = {"theme": "white"}

# Mail
MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USERNAME = "SomeBlocks Info"
DEFAULT_MAIL_SENDER = "noreply@someblocks.com"

# App specific configurations
## RSS
RSS_MCUPDATES = "http://mcupdate.tumblr.com/rss"

## Minecraft Query
MC_SERVER = "someblocks.com"
MC_PORT = 25565

# I have disabled the registration on my server (this is only temporary)
REGISTRATION = True
