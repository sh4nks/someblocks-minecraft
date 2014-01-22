from datetime import datetime

from flask import Flask, render_template
from flask.ext.login import current_user

from .extensions import db, login_manager, mail, misaka, cache
from .models.users import User
from .models.pages import Page
from .utils import format_date

__version__ = "0.2"


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("settings")
    app.config.from_object(config)
    app.config.from_envvar("SOMEBLOCKS_SETTINGS", silent=True)

    configure_blueprints(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_before_request(app)
    configure_errorhandlers(app)
    return app


def configure_blueprints(app):
    from .views import admin, users, frontend, auth, blog
    app.register_blueprint(admin.mod, url_prefix=app.config["ADMIN_URL"])
    app.register_blueprint(users.mod, url_prefix=app.config["USER_URL"])
    app.register_blueprint(frontend.mod, url_prefix=app.config["FRONTEND_URL"])
    app.register_blueprint(auth.mod, url_prefix=app.config["AUTH_URL"])
    app.register_blueprint(blog.mod, url_prefix=app.config["BLOG_URL"])


def configure_extensions(app):
    # Database
    db.init_app(app)
    # Mail
    mail.init_app(app)
    # Markdown
    misaka.init_app(app)
    # Caching
    cache.init_app(app)

    # Login
    login_manager.init_app(app)
    login_manager.login_view = app.config.get('AUTH_LOGIN_VIEW')

    @login_manager.user_loader
    def load_user(uid):
        """
        This is required by the Flask-Login extension
        """
        return User.query.get(int(uid))


def configure_template_filters(app):
    app.jinja_env.filters['datetime'] = format_date


def configure_context_processors(app):
    @app.context_processor
    def create_navigation():
        pages = Page.query.order_by(Page.position.asc())
        return dict(pages=pages)


def configure_before_request(app):
    @app.before_request
    def before_request():
        """
        Updates `lastvisit` before every reguest if the user is authenticated
        """
        if current_user.is_authenticated():
            current_user.lastvisit = datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()


def configure_errorhandlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500
