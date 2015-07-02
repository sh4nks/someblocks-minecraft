from flask import Flask, render_template

from someblocks.gaming.views import gaming
from someblocks.main.views import main
from someblocks.extensions import cache
from someblocks.utils import format_date


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object("someblocks.configs.default")
    app.config.from_object(config)
    app.config.from_envvar("SOMEBLOCKS_SETTINGS", silent=True)

    configure_blueprints(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_errorhandlers(app)
    return app


def configure_blueprints(app):
    app.register_blueprint(main, url_prefix=app.config["MAIN_URL"])
    app.register_blueprint(gaming,
                           url_prefix=app.config.get("GAMING_URL", ""),
                           subdomain=app.config.get("GAMING_SUBDOMAIN", ""))


def configure_extensions(app):
    # Caching
    cache.init_app(app)


def configure_template_filters(app):
    app.jinja_env.filters['datetime'] = format_date


def configure_errorhandlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500
