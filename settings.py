import os
_basedir = os.path.abspath(os.path.dirname(__file__))

# Indicates that it is a dev environment
DEBUG = True
SECRET_KEY = 'SecretKeyForSessionSigning'

# SQLAlchemy connection options
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
DATABASE_CONNECT_OPTIONS = {}

# Protection against form post fraud
CSRF_ENABLED=True
CSRF_SESSION_KEY="reallyhardtoguess"

# Auth
AUTH_USER_MIXINS = []
AUTH_LOGIN_VIEW = 'users.login'

# Bootstrap
BOOTSTRAP_USE_MINIFIED = False
BOOTSTRAP_USE_CDN = False

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = "6LfUZ9YSAAAAANtDdyew22z2lnjz-K0Dx8M-gkey"
RECAPTCHA_PRIVATE_KEY= "6LfUZ9YSAAAAAHgDBflMFQTVdlTA3__yYx8CBGII"
RECAPTCHA_OPTIONS = {"theme": "white"}

# TODO: Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'password_here'
DEFAULT_MAIL_SENDER = 'Admin <%s>' % MAIL_USERNAME

# App specific configurations
RSS_MCUPDATES = 'http://mcupdate.tumblr.com/rss'