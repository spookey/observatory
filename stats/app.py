from flask import Flask

from stats.lib.cli import BP_CLI
from stats.rest.sensor import BP_REST_SENSOR
from stats.shared import errorhandler, tagline
from stats.start.environment import ERROR_CODES, MDL_NAME
from stats.start.extensions import (
    BCRYPT, CSRF_PROTECT, DB, LOGIN_MANAGER, MIGRATE, REST
)
from stats.start.logger import initialize_logging
from stats.views.main import BLUEPRINT_MAIN
from stats.views.mgnt import BLUEPRINT_MGNT
from stats.views.side import BLUEPRINT_SIDE
from stats.views.user import BLUEPRINT_USER


def create_app(config_obj):
    initialize_logging()

    app = Flask(MDL_NAME)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)
    register_template_functions(app)

    return app


def register_extensions(app):
    BCRYPT.init_app(app)
    CSRF_PROTECT.init_app(app)
    DB.init_app(app)
    LOGIN_MANAGER.init_app(app)
    MIGRATE.init_app(app, DB)
    REST.init_app(app)


def register_errorhandlers(app):
    for code in ERROR_CODES:
        app.errorhandler(code)(errorhandler)


def register_blueprints(app):
    app.register_blueprint(BP_CLI)
    app.register_blueprint(BLUEPRINT_MAIN)
    app.register_blueprint(BLUEPRINT_MGNT)
    app.register_blueprint(BLUEPRINT_SIDE)
    app.register_blueprint(BLUEPRINT_USER)
    app.register_blueprint(BP_REST_SENSOR)


def register_template_functions(app):
    app.jinja_env.globals.update(
        tagline=tagline
    )
