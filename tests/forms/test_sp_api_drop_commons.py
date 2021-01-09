from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_drop import (
    SpaceDropCamForm,
    SpaceDropContactKeymastersForm,
    SpaceDropLinksForm,
    SpaceDropMembershipPlansForm,
    SpaceDropProjectsForm,
    SpaceDropSensorsBarometerForm,
    SpaceDropSensorsBeverageSupplyForm,
    SpaceDropSensorsDoorLockedForm,
    SpaceDropSensorsHumidityForm,
    SpaceDropSensorsTemperatureForm,
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
            'sensors.temperature.value.horizon',
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
            'sensors.door_locked.value.horizon',
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
            'sensors.barometer.value.horizon',
            'sensors.barometer.unit',
            'sensors.barometer.location',
            'sensors.barometer.name',
            'sensors.barometer.description',
        ],
    ),
    form_drop(
        SpaceDropSensorsHumidityForm,
        keys=[
            'sensors.humidity.value',
            'sensors.humidity.value.elevate',
            'sensors.humidity.value.convert',
            'sensors.humidity.value.horizon',
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
            'sensors.beverage_supply.value.horizon',
            'sensors.beverage_supply.unit',
            'sensors.beverage_supply.location',
            'sensors.beverage_supply.name',
            'sensors.beverage_supply.description',
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
