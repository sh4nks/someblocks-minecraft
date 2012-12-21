from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.bootstrap import Bootstrap
from flask.ext.misaka import Misaka
from flask.ext.cache import Cache

from datetime import datetime

app = Flask(__name__)
app.config.from_object("settings")

# Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = app.config.get('AUTH_LOGIN_VIEW')
# Database
db = SQLAlchemy(app)
# Mail
mail = Mail(app)
# Bootstrap
Bootstrap(app)
# Markdown
Misaka(app)
# Caching
cache = Cache()
cache.init_app(app)


from app.views import admin, users, frontend, blog
app.register_blueprint(admin.mod)
app.register_blueprint(users.mod)
app.register_blueprint(frontend.mod)
app.register_blueprint(blog.mod)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

def format_date(value, format='normal'):
    if format == 'normal':
        format = '%d.%m.%Y @ %H:%M'
    elif format == 'alphabet':
        format = '%b %d %Y'
    return value.strftime(format)
app.jinja_env.filters['datetime'] = format_date
