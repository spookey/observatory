from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
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
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def form_drop(form, *, keys):
    def res():
        pass

    res.form = form
    res.keys = keys

    return res


FORMS = [
    form_drop(
        SpaceDropCamForm,
        keys=['cam'],
    ),
    form_drop(
        SpaceDropContactKeymastersForm,
        keys=[
            'contact.keymasters.name',
            'contact.keymasters.irc_nick',
            'contact.keymasters.phone',
            'contact.keymasters.email',
            'contact.keymasters.twitter',
            'contact.keymasters.xmpp',
            'contact.keymasters.mastodon',
            'contact.keymasters.matrix',
        ],
    ),
    form_drop(
        SpaceDropSensorsTemperatureForm,
        keys=[
            'sensors.temperature.value',
            'sensors.temperature.value.elevate',
            'sensors.temperature.value.convert',
            'sensors.temperature.unit',
            'sensors.temperature.location',
            'sensors.temperature.name',
            'sensors.temperature.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsDoorLockedForm,
        keys=[
            'sensors.door_locked.value',
            'sensors.door_locked.value.elevate',
            'sensors.door_locked.value.convert',
            'sensors.door_locked.location',
            'sensors.door_locked.name',
            'sensors.door_locked.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsBarometerForm,
        keys=[
            'sensors.barometer.value',
            'sensors.barometer.value.elevate',
            'sensors.barometer.value.convert',
            'sensors.barometer.unit',
            'sensors.barometer.location',
            'sensors.barometer.name',
            'sensors.barometer.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsRadiationAlphaForm,
        keys=[
            'sensors.radiation.alpha.value',
            'sensors.radiation.alpha.value.elevate',
            'sensors.radiation.alpha.value.convert',
            'sensors.radiation.alpha.unit',
            'sensors.radiation.alpha.dead_time',
            'sensors.radiation.alpha.conversion_factor',
            'sensors.radiation.alpha.location',
            'sensors.radiation.alpha.name',
            'sensors.radiation.alpha.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsRadiationBetaForm,
        keys=[
            'sensors.radiation.beta.value',
            'sensors.radiation.beta.value.elevate',
            'sensors.radiation.beta.value.convert',
            'sensors.radiation.beta.unit',
            'sensors.radiation.beta.dead_time',
            'sensors.radiation.beta.conversion_factor',
            'sensors.radiation.beta.location',
            'sensors.radiation.beta.name',
            'sensors.radiation.beta.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsRadiationGammaForm,
        keys=[
            'sensors.radiation.gamma.value',
            'sensors.radiation.gamma.value.elevate',
            'sensors.radiation.gamma.value.convert',
            'sensors.radiation.gamma.unit',
            'sensors.radiation.gamma.dead_time',
            'sensors.radiation.gamma.conversion_factor',
            'sensors.radiation.gamma.location',
            'sensors.radiation.gamma.name',
            'sensors.radiation.gamma.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsRadiationBetaGammaForm,
        keys=[
            'sensors.radiation.beta_gamma.value',
            'sensors.radiation.beta_gamma.value.elevate',
            'sensors.radiation.beta_gamma.value.convert',
            'sensors.radiation.beta_gamma.unit',
            'sensors.radiation.beta_gamma.dead_time',
            'sensors.radiation.beta_gamma.conversion_factor',
            'sensors.radiation.beta_gamma.location',
            'sensors.radiation.beta_gamma.name',
            'sensors.radiation.beta_gamma.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsHumidityForm,
        keys=[
            'sensors.humidity.value',
            'sensors.humidity.value.elevate',
            'sensors.humidity.value.convert',
            'sensors.humidity.unit',
            'sensors.humidity.location',
            'sensors.humidity.name',
            'sensors.humidity.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsBeverageSupplyForm,
        keys=[
            'sensors.beverage_supply.value',
            'sensors.beverage_supply.value.elevate',
            'sensors.beverage_supply.value.convert',
            'sensors.beverage_supply.unit',
            'sensors.beverage_supply.location',
            'sensors.beverage_supply.name',
            'sensors.beverage_supply.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsPowerConsumptionForm,
        keys=[
            'sensors.power_consumption.value',
            'sensors.power_consumption.value.elevate',
            'sensors.power_consumption.value.convert',
            'sensors.power_consumption.unit',
            'sensors.power_consumption.location',
            'sensors.power_consumption.name',
            'sensors.power_consumption.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsWindForm,
        keys=[
            'sensors.wind.properties.speed.value',
            'sensors.wind.properties.speed.value.elevate',
            'sensors.wind.properties.speed.value.convert',
            'sensors.wind.properties.speed.unit',
            'sensors.wind.properties.gust.value',
            'sensors.wind.properties.gust.value.elevate',
            'sensors.wind.properties.gust.value.convert',
            'sensors.wind.properties.gust.unit',
            'sensors.wind.properties.direction.value',
            'sensors.wind.properties.direction.value.elevate',
            'sensors.wind.properties.direction.value.convert',
            'sensors.wind.properties.direction.unit',
            'sensors.wind.properties.elevation.value',
            'sensors.wind.properties.elevation.value.elevate',
            'sensors.wind.properties.elevation.value.convert',
            'sensors.wind.properties.elevation.unit',
            'sensors.wind.location',
            'sensors.wind.name',
            'sensors.wind.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsAccountBalanceForm,
        keys=[
            'sensors.account_balance.value',
            'sensors.account_balance.value.elevate',
            'sensors.account_balance.value.convert',
            'sensors.account_balance.unit',
            'sensors.account_balance.location',
            'sensors.account_balance.name',
            'sensors.account_balance.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsTotalMemberCountForm,
        keys=[
            'sensors.total_member_count.value',
            'sensors.total_member_count.value.elevate',
            'sensors.total_member_count.value.convert',
            'sensors.total_member_count.location',
            'sensors.total_member_count.name',
            'sensors.total_member_count.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsNetworkTrafficForm,
        keys=[
            'sensors.network_traffic.properties.bits_per_second.value',
            'sensors.network_traffic.properties.bits_per_second.value.elevate',
            'sensors.network_traffic.properties.bits_per_second.value.convert',
            'sensors.network_traffic.properties.bits_per_second.maximum',
            'sensors.network_traffic.properties.packets_per_second.value',
            (
                'sensors.network_traffic.properties.'
                'packets_per_second.value.elevate'
            ),
            (
                'sensors.network_traffic.properties.'
                'packets_per_second.value.convert'
            ),
            'sensors.network_traffic.location',
            'sensors.network_traffic.name',
            'sensors.network_traffic.description',
        ],
    ),
    form_drop(
        SpaceDropProjectsForm,
        keys=['projects'],
    ),
    form_drop(
        SpaceDropLinksForm,
        keys=[
            'links.name',
            'links.description',
            'links.url',
        ],
    ),
    form_drop(
        SpaceDropMembershipPlansForm,
        keys=[
            'membership_plans.name',
            'membership_plans.value',
            'membership_plans.currency',
            'membership_plans.billing_interval',
            'membership_plans.description',
        ],
    ),
]
IDS = [drop.form.__name__ for drop in FORMS]


@mark.usefixtures('session', 'ctx_app')
class TestSpaceDropCommons:
    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_edit_keys(drop):
        assert drop.form.KEYS == drop.keys

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_basic_fields(drop):
        form = drop.form(idx=0)
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_form_idx(drop):
        idx = choice(range(23, 42))
        form = drop.form(idx=idx)
        assert form.idx == idx

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_submit_button(drop):
        idx = choice(range(23, 42))
        form = drop.form(idx=idx)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_delete'
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-danger is-small'
        }

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_invalid(drop):
        form = drop.form(idx=None)
        assert form.validate() is False
        assert form.action() is None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_empty_action(drop):
        form = drop.form(idx=0)
        assert form.validate() is True
        assert form.action() is None

    @staticmethod
    @mark.parametrize('drop', FORMS, ids=IDS)
    def test_delete(drop):
        idx = choice(range(23, 42))
        elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}',
                idx=idx,
                elem=choice(
                    [
                        choice(['test', 'demo']),
                        choice([True, False]),
                        choice(range(23, 42)),
                    ]
                ),
            )
            for key in drop.keys
        ]

        assert Value.query.all() == elems

        form = drop.form(idx=idx, submit=True)
        assert form.validate() is True
        assert form.action()

        assert Value.query.all() == []
