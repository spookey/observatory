from flask_wtf import FlaskForm
from wtforms import SubmitField

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.instance import SPACE_API
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX

# pylint: disable=arguments-differ
# pylint: disable=no-member


class SpaceDropForm(FlaskForm):
    KEYS = []

    submit = SubmitField(
        'Delete',
        description='Submit',
        widget=SubmitButtonInput(
            icon='ops_delete',
            classreplace_kw={'is-dark': 'is-danger is-small'},
        ),
    )

    def __init__(self, *args, idx, **kwargs):
        super().__init__(*args, **kwargs)
        self.idx = idx

    def validate(self):
        return super().validate() and self.idx is not None

    def action(self):
        if not self.validate():
            return None

        results = [
            elem.delete()
            for elem in [
                Value.by_key_idx(key=f'{SP_API_PREFIX}.{key}', idx=self.idx)
                for key in self.KEYS
            ]
            if elem is not None
        ]

        if not any(results):
            return None

        return SPACE_API.reset()


class SpaceDropCamForm(SpaceDropForm):
    KEYS = ['cam']


class SpaceDropContactKeymastersForm(SpaceDropForm):
    KEYS = [
        'contact.keymasters.name',
        'contact.keymasters.irc_nick',
        'contact.keymasters.phone',
        'contact.keymasters.email',
        'contact.keymasters.twitter',
        'contact.keymasters.xmpp',
        'contact.keymasters.mastodon',
        'contact.keymasters.matrix',
    ]


class SpaceDropSensorsTemperatureForm(SpaceDropForm):
    KEYS = [
        'sensors.temperature.value',
        'sensors.temperature.value.elevate',
        'sensors.temperature.value.convert',
        'sensors.temperature.value.horizon',
        'sensors.temperature.unit',
        'sensors.temperature.location',
        'sensors.temperature.name',
        'sensors.temperature.description',
    ]


class SpaceDropSensorsDoorLockedForm(SpaceDropForm):
    KEYS = [
        'sensors.door_locked.value',
        'sensors.door_locked.value.elevate',
        'sensors.door_locked.value.convert',
        'sensors.door_locked.value.horizon',
        'sensors.door_locked.location',
        'sensors.door_locked.name',
        'sensors.door_locked.description',
    ]


class SpaceDropSensorsBarometerForm(SpaceDropForm):
    KEYS = [
        'sensors.barometer.value',
        'sensors.barometer.value.elevate',
        'sensors.barometer.value.convert',
        'sensors.barometer.value.horizon',
        'sensors.barometer.unit',
        'sensors.barometer.location',
        'sensors.barometer.name',
        'sensors.barometer.description',
    ]


class SpaceDropSensorsHumidityForm(SpaceDropForm):
    KEYS = [
        'sensors.humidity.value',
        'sensors.humidity.value.elevate',
        'sensors.humidity.value.convert',
        'sensors.humidity.value.horizon',
        'sensors.humidity.unit',
        'sensors.humidity.location',
        'sensors.humidity.name',
        'sensors.humidity.description',
    ]


class SpaceDropSensorsBeverageSupplyForm(SpaceDropForm):
    KEYS = [
        'sensors.beverage_supply.value',
        'sensors.beverage_supply.value.elevate',
        'sensors.beverage_supply.value.convert',
        'sensors.beverage_supply.value.horizon',
        'sensors.beverage_supply.unit',
        'sensors.beverage_supply.location',
        'sensors.beverage_supply.name',
        'sensors.beverage_supply.description',
    ]


class SpaceDropSensorsPowerConsumptionForm(SpaceDropForm):
    KEYS = [
        'sensors.power_consumption.value',
        'sensors.power_consumption.value.elevate',
        'sensors.power_consumption.value.convert',
        'sensors.power_consumption.value.horizon',
        'sensors.power_consumption.unit',
        'sensors.power_consumption.location',
        'sensors.power_consumption.name',
        'sensors.power_consumption.description',
    ]


class SpaceDropProjectsForm(SpaceDropForm):
    KEYS = ['projects']


class SpaceDropLinksForm(SpaceDropForm):
    KEYS = [
        'links.name',
        'links.description',
        'links.url',
    ]


class SpaceDropMembershipPlansForm(SpaceDropForm):
    KEYS = [
        'membership_plans.name',
        'membership_plans.value',
        'membership_plans.currency',
        'membership_plans.billing_interval',
        'membership_plans.description',
    ]
