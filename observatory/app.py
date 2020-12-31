from flask import Flask

from observatory.lib.cli import BP_CLI
from observatory.rest.charts import BP_REST_CHARTS
from observatory.rest.mapper import BP_REST_MAPPER
from observatory.rest.owners import BP_REST_OWNERS
from observatory.rest.prompt import BP_REST_PROMPT
from observatory.rest.sensor import BP_REST_SENSOR
from observatory.rest.sp_api import BP_REST_SP_API
from observatory.shared import (
    SPACE_API,
    errorhandler,
    form_drop_mapper,
    form_drop_prompt,
    form_drop_sensor,
    form_sort_mapper,
    form_sort_prompt,
    form_sort_sensor,
    script_config_data,
    tagline,
)
from observatory.start.environment import ERROR_CODES, MDL_NAME
from observatory.start.extensions import (
    BCRYPT,
    CSRF_PROTECT,
    DB,
    LOGIN_MANAGER,
    MIGRATE,
    REST,
)
from observatory.start.logger import initialize_logging
from observatory.views.main import BLUEPRINT_MAIN
from observatory.views.mgnt import BLUEPRINT_MGNT
from observatory.views.sapi import BLUEPRINT_SAPI
from observatory.views.side import BLUEPRINT_SIDE
from observatory.views.user import BLUEPRINT_USER


def create_app(config_obj):
    initialize_logging()

    app = Flask(MDL_NAME)
    app.config.from_object(config_obj)

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)
    register_template_functions(app)

    configure_jinja(app)

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
    app.register_blueprint(BLUEPRINT_SAPI)
    app.register_blueprint(BLUEPRINT_SIDE)
    app.register_blueprint(BLUEPRINT_USER)
    app.register_blueprint(BP_REST_CHARTS)
    app.register_blueprint(BP_REST_MAPPER)
    app.register_blueprint(BP_REST_OWNERS)
    app.register_blueprint(BP_REST_PROMPT)
    app.register_blueprint(BP_REST_SENSOR)
    app.register_blueprint(BP_REST_SP_API)


def register_template_functions(app):
    app.jinja_env.globals.update(
        form_drop_mapper=form_drop_mapper,
        form_drop_prompt=form_drop_prompt,
        form_drop_sensor=form_drop_sensor,
        form_sort_mapper=form_sort_mapper,
        form_sort_prompt=form_sort_prompt,
        form_sort_sensor=form_sort_sensor,
        script_config_data=script_config_data,
        space_api=SPACE_API,
        tagline=tagline,
    )


def configure_jinja(app):
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
