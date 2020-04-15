from observatory.lib.cli import BP_CLI
from observatory.rest.mapper import BP_REST_MAPPER
from observatory.rest.prompt import BP_REST_PROMPT
from observatory.rest.sensor import BP_REST_SENSOR
from observatory.shared import (
    errorhandler, form_drop_mapper, form_drop_prompt, form_drop_sensor,
    form_sort_mapper, form_sort_prompt, form_sort_sensor, moment_config,
    tagline
)
from observatory.start.environment import ERROR_CODES
from observatory.start.extensions import CSRF_PROTECT, DB, MIGRATE
from observatory.views.main import BLUEPRINT_MAIN
from observatory.views.mgnt import BLUEPRINT_MGNT
from observatory.views.side import BLUEPRINT_SIDE
from observatory.views.user import BLUEPRINT_USER


class TestApp:

    @staticmethod
    def test_extensions(app):
        assert app.extensions['csrf'] == CSRF_PROTECT

        mig_conf = app.extensions['migrate']
        assert mig_conf.migrate == MIGRATE

        sql_stat = app.extensions['sqlalchemy']
        assert sql_stat.db == DB

    @staticmethod
    def test_errorhandler(app):
        handlers = app.error_handler_spec[None]
        for code in ERROR_CODES:
            for handler in handlers[code].values():
                assert handler is errorhandler

    @staticmethod
    def test_blueprints(app):
        blueprints = [
            BP_CLI,
            BLUEPRINT_MAIN, BLUEPRINT_MGNT,
            BLUEPRINT_SIDE, BLUEPRINT_USER,
            BP_REST_MAPPER, BP_REST_PROMPT, BP_REST_SENSOR,
        ]
        for blueprint in app.blueprints.values():
            assert blueprint in blueprints
            blueprints.remove(blueprint)

        assert not blueprints

    @staticmethod
    def test_template_functions(app):
        for func in (
                form_drop_mapper,
                form_drop_prompt,
                form_drop_sensor,
                form_sort_mapper,
                form_sort_prompt,
                form_sort_sensor,
                moment_config,
                tagline,
        ):
            assert app.jinja_env.globals[func.__name__] is func

    @staticmethod
    def test_jinja_config(app):
        assert app.jinja_env.lstrip_blocks is True
        assert app.jinja_env.trim_blocks is True
