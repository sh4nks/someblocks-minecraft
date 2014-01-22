from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.misaka import Misaka
from flask.ext.cache import Cache

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
misaka = Misaka()
cache = Cache()
