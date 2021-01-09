from observatory.instance import SPACE_API
from observatory.lib.cli import BP_CLI
from observatory.rest.charts import BP_REST_CHARTS
from observatory.rest.mapper import BP_REST_MAPPER
from observatory.rest.owners import BP_REST_OWNERS
from observatory.rest.prompt import BP_REST_PROMPT
from observatory.rest.sensor import BP_REST_SENSOR
from observatory.rest.sp_api import BP_REST_SP_API
from observatory.shared import (
    errorhandler,
    form_drop_mapper,
    form_drop_prompt,
    form_drop_sensor,
    form_drop_space_cam,
    form_drop_space_contact_keymasters,
    form_drop_space_links,
    form_drop_space_membership_plans,
    form_drop_space_projects,
    form_drop_space_sensors_account_balance,
    form_drop_space_sensors_barometer,
    form_drop_space_sensors_beverage_supply,
    form_drop_space_sensors_humidity,
    form_drop_space_sensors_power_consumption,
    form_sort_mapper,
    form_sort_prompt,
    form_sort_sensor,
    script_config_data,
    tagline,
)
from observatory.start.environment import ERROR_CODES
from observatory.start.extensions import CSRF_PROTECT, DB, MIGRATE
from observatory.views.main import BLUEPRINT_MAIN
from observatory.views.mgnt import BLUEPRINT_MGNT
from observatory.views.sapi import BLUEPRINT_SAPI
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
            BLUEPRINT_MAIN,
            BLUEPRINT_MGNT,
            BLUEPRINT_SAPI,
            BLUEPRINT_SIDE,
            BLUEPRINT_USER,
            BP_CLI,
            BP_REST_CHARTS,
            BP_REST_MAPPER,
            BP_REST_OWNERS,
            BP_REST_PROMPT,
            BP_REST_SENSOR,
            BP_REST_SP_API,
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
            form_drop_space_cam,
            form_drop_space_contact_keymasters,
            form_drop_space_links,
            form_drop_space_membership_plans,
            form_drop_space_projects,
            form_drop_space_sensors_account_balance,
            form_drop_space_sensors_barometer,
            form_drop_space_sensors_beverage_supply,
            form_drop_space_sensors_humidity,
            form_drop_space_sensors_power_consumption,
            form_sort_mapper,
            form_sort_prompt,
            form_sort_sensor,
            script_config_data,
            tagline,
        ):
            assert app.jinja_env.globals[func.__name__] is func

        assert app.jinja_env.globals['space_api'] is SPACE_API

    @staticmethod
    def test_jinja_config(app):
        assert app.jinja_env.lstrip_blocks is True
        assert app.jinja_env.trim_blocks is True
