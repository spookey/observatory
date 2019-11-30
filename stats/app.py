from flask import Flask

from stats.shared import errorhandler
from stats.start.environment import ERROR_CODES, MDL_NAME
from stats.start.extensions import CSRF_PROTECT, DB, MIGRATE
from stats.start.logger import initialize_logging
from stats.views.side import BLUEPRINT_SIDE


def create_app(config_obj):
    initialize_logging()

    app = Flask(MDL_NAME)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    CSRF_PROTECT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)


def register_errorhandlers(app):
    for code in ERROR_CODES:
        app.errorhandler(code)(errorhandler)


def register_blueprints(app):
#     app.register_blueprint(BLUEPRINT_MAIN)
    app.register_blueprint(BLUEPRINT_SIDE)
