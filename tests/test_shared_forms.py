from collections import namedtuple
from random import choice

from pytest import fixture, mark

from observatory.forms.common import (
    PromptDropForm,
    PromptSortForm,
    SensorDropForm,
    SensorSortForm,
)
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.forms.space_drop import (
    SpaceDropCamForm,
    SpaceDropContactKeymastersForm,
    SpaceDropLinksForm,
    SpaceDropMembershipPlansForm,
    SpaceDropProjectsForm,
    SpaceDropSensorsAccountBalanceForm,
    SpaceDropSensorsBarometerForm,
    SpaceDropSensorsBeverageSupplyForm,
    SpaceDropSensorsDoorLockedForm,
    SpaceDropSensorsHumidityForm,
    SpaceDropSensorsNetworkTrafficForm,
    SpaceDropSensorsPowerConsumptionForm,
    SpaceDropSensorsRadiationAlphaForm,
    SpaceDropSensorsRadiationBetaForm,
    SpaceDropSensorsRadiationBetaGammaForm,
    SpaceDropSensorsRadiationGammaForm,
    SpaceDropSensorsTemperatureForm,
    SpaceDropSensorsTotalMemberCountForm,
    SpaceDropSensorsWindForm,
)
from observatory.models.mapper import Mapper
from observatory.shared import (
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
    form_drop_space_sensors_door_locked,
    form_drop_space_sensors_humidity,
    form_drop_space_sensors_network_traffic,
    form_drop_space_sensors_power_consumption,
    form_drop_space_sensors_radiation_alpha,
    form_drop_space_sensors_radiation_beta,
    form_drop_space_sensors_radiation_beta_gamma,
    form_drop_space_sensors_radiation_gamma,
    form_drop_space_sensors_temperature,
    form_drop_space_sensors_total_member_count,
    form_drop_space_sensors_wind,
    form_sort_mapper,
    form_sort_prompt,
    form_sort_sensor,
)

SpaceDrop = namedtuple('SpaceDrop', ('func', 'form'))

SPACE_DROP_FORMS = [
    SpaceDrop(
        func=form_drop_space_cam,
        form=SpaceDropCamForm,
    ),
    SpaceDrop(
        func=form_drop_space_contact_keymasters,
        form=SpaceDropContactKeymastersForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_temperature,
        form=SpaceDropSensorsTemperatureForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_door_locked,
        form=SpaceDropSensorsDoorLockedForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_barometer,
        form=SpaceDropSensorsBarometerForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_radiation_alpha,
        form=SpaceDropSensorsRadiationAlphaForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_radiation_beta,
        form=SpaceDropSensorsRadiationBetaForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_radiation_gamma,
        form=SpaceDropSensorsRadiationGammaForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_radiation_beta_gamma,
        form=SpaceDropSensorsRadiationBetaGammaForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_humidity,
        form=SpaceDropSensorsHumidityForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_beverage_supply,
        form=SpaceDropSensorsBeverageSupplyForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_power_consumption,
        form=SpaceDropSensorsPowerConsumptionForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_wind,
        form=SpaceDropSensorsWindForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_account_balance,
        form=SpaceDropSensorsAccountBalanceForm,
    ),
    SpaceDrop(
        func=form_drop_space_sensors_total_member_count,
        form=SpaceDropSensorsTotalMemberCountForm,
    ),
    SpaceDrop(
        form=SpaceDropSensorsNetworkTrafficForm,
        func=form_drop_space_sensors_network_traffic,
    ),
    SpaceDrop(
        func=form_drop_space_links,
        form=SpaceDropLinksForm,
    ),
    SpaceDrop(
        func=form_drop_space_membership_plans,
        form=SpaceDropMembershipPlansForm,
    ),
    SpaceDrop(
        func=form_drop_space_projects,
        form=SpaceDropProjectsForm,
    ),
]
SPACE_DROP_IDS = [space_form.form.__name__ for space_form in SPACE_DROP_FORMS]


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _drop(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.func, res.form, res.gen_common = {
        'prompt': (form_drop_prompt, PromptDropForm, gen_prompt),
        'sensor': (form_drop_sensor, SensorDropForm, gen_sensor),
        'mapper': (
            form_drop_mapper,
            MapperDropForm,
            lambda: Mapper.create(prompt=gen_prompt(), sensor=gen_sensor()),
        ),
    }.get(request.param)

    yield res


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _sort(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.func, res.form, res.gen_common = {
        'prompt': (form_sort_prompt, PromptSortForm, gen_prompt),
        'sensor': (form_sort_sensor, SensorSortForm, gen_sensor),
        'mapper': (
            form_sort_mapper,
            MapperSortForm,
            lambda: Mapper.create(prompt=gen_prompt(), sensor=gen_sensor()),
        ),
    }.get(request.param)

    yield res


@mark.usefixtures('session')
class TestSharedForms:
    @staticmethod
    def test_drop_generic_empty(_drop):
        form = _drop.func(None)
        assert isinstance(form, _drop.form)
        assert form.thing is None
        assert form.validate() is False

    @staticmethod
    def test_drop_generic(_drop):
        thing = _drop.gen_common()
        form = _drop.func(thing)
        assert isinstance(form, _drop.form)
        assert form.thing == thing
        assert form.validate() is True

    @staticmethod
    def test_sort_generic_empty(_sort):
        form = _sort.func(None, None)
        assert isinstance(form, _sort.form)
        assert form.thing is None
        assert form.lift is None
        assert form.validate() is False

    @staticmethod
    def test_sort_generic(_sort):
        thing = _sort.gen_common()
        form = _sort.func(thing, True)
        assert isinstance(form, _sort.form)
        assert form.thing == thing
        assert form.lift is True
        assert form.validate() is True

    @staticmethod
    @mark.parametrize('_drop', SPACE_DROP_FORMS)
    def test_drop_space(_drop):
        idx = choice(range(23, 42))
        form = _drop.func(idx=idx)
        assert isinstance(form, _drop.form)
        assert form.idx == idx
        assert form.validate() is True
        assert form.KEYS
