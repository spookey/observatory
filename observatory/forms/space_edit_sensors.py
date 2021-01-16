from wtforms import (
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange, Optional

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_edit import SpaceEditForm
from observatory.models.sensor import Sensor

# pylint: disable=arguments-differ
# pylint: disable=no-member


class SpaceEditSensorsForm(SpaceEditForm):
    KEYS = {}
    SENSORS = []

    @staticmethod
    def _sensor_field(label):
        return SelectField(
            label,
            coerce=int,
            validators=[DataRequired()],
            description='Select sensor',
        )

    @staticmethod
    def _sensor_choices():
        return [
            (sensor.prime, f'{sensor.slug} ({sensor.title})')
            for sensor in Sensor.query.order_by('slug').all()
        ]

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)

        for key in self.SENSORS:
            sensor_sel = getattr(self, key, None)
            if sensor_sel:
                sensor_sel.choices = self._sensor_choices()


class SpaceEditSensorsTemperatureForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.temperature.value',
        unit_sel='sensors.temperature.unit',
        location='sensors.temperature.location',
        name='sensors.temperature.name',
        description='sensors.temperature.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Temperature sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[
            (val, val)
            for val in ('°C', '°F', 'K', '°De', '°N', '°R', '°Ré', '°Rø')
        ],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsDoorLockedForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.door_locked.value',
        location='sensors.door_locked.location',
        name='sensors.door_locked.name',
        description='sensors.door_locked.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Door lock sensor')
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsBarometerForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.barometer.value',
        unit_sel='sensors.barometer.unit',
        location='sensors.barometer.location',
        name='sensors.barometer.name',
        description='sensors.barometer.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Barometer')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('hPa', 'hPA')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsRadiationForm(SpaceEditSensorsForm):
    KEYS = []
    SENSORS = ['sensor_sel']

    @staticmethod
    def create(sub):
        return dict(
            sensor_sel=f'sensors.radiation.{sub}.value',
            unit_sel=f'sensors.radiation.{sub}.unit',
            dead_time=f'sensors.radiation.{sub}.dead_time',
            conversion_factor=f'sensors.radiation.{sub}.conversion_factor',
            location=f'sensors.radiation.{sub}.location',
            name=f'sensors.radiation.{sub}.name',
            description=f'sensors.radiation.{sub}.description',
        )

    sensor_sel = SpaceEditSensorsForm._sensor_field('Radiation sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[
            (val, val) for val in ('cpm', 'r/h', 'µSv/h', 'mSv/a', 'µSv/a')
        ],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    dead_time = DecimalField(
        'Dead time',
        default=1.0,
        places=6,
        validators=[NumberRange(min=0.0)],
        description='The dead time in µs',
    )
    conversion_factor = DecimalField(
        'Conversion factor',
        default=1.0,
        places=6,
        validators=[NumberRange(min=0.0)],
        description='Conversion from the cpm unit to another unit',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsRadiationAlphaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('alpha')


class SpaceEditSensorsRadiationBetaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('beta')


class SpaceEditSensorsRadiationGammaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('gamma')


class SpaceEditSensorsRadiationBetaGammaForm(SpaceEditSensorsRadiationForm):
    KEYS = SpaceEditSensorsRadiationForm.create('beta_gamma')


class SpaceEditSensorsHumidityForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.humidity.value',
        unit_sel='sensors.humidity.unit',
        location='sensors.humidity.location',
        name='sensors.humidity.name',
        description='sensors.humidity.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Humidity sensor')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('%', '%')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsBeverageSupplyForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.beverage_supply.value',
        unit_sel='sensors.beverage_supply.unit',
        location='sensors.beverage_supply.location',
        name='sensors.beverage_supply.name',
        description='sensors.beverage_supply.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field(
        'How much Mate and beer is in your fridge?'
    )
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('btl', 'Bottles'), ('crt', 'Crates')],
        validators=[DataRequired()],
        description='The unit (bottles or crates)',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='Where do you hide your gems',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='What is it',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsPowerConsumptionForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.power_consumption.value',
        unit_sel='sensors.power_consumption.unit',
        location='sensors.power_consumption.location',
        name='sensors.power_consumption.name',
        description='sensors.power_consumption.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Power consumption')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('mW', 'W', 'VA')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsWindForm(SpaceEditSensorsForm):
    KEYS = dict(
        speed_sensor_sel='sensors.wind.properties.speed.value',
        speed_unit_sel='sensors.wind.properties.speed.unit',
        gust_sensor_sel='sensors.wind.properties.gust.value',
        gust_unit_sel='sensors.wind.properties.gust.unit',
        direction_sensor_sel='sensors.wind.properties.direction.value',
        direction_unit_sel='sensors.wind.properties.direction.unit',
        elevation_value='sensors.wind.properties.elevation.value',
        elevation_unit_sel='sensors.wind.properties.elevation.unit',
        location='sensors.wind.location',
        name='sensors.wind.name',
        description='sensors.wind.description',
    )
    SENSORS = [
        'speed_sensor_sel',
        'gust_sensor_sel',
        'direction_sensor_sel',
    ]

    speed_sensor_sel = SpaceEditSensorsForm._sensor_field('Wind speed sensor')
    speed_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('m/s', 'km/h', 'kn')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    gust_sensor_sel = SpaceEditSensorsForm._sensor_field('Wind gust sensor')
    gust_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[(val, val) for val in ('m/s', 'km/h', 'kn')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    direction_sensor_sel = SpaceEditSensorsForm._sensor_field(
        'Wind direction sensor'
    )
    direction_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('°', '°')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    elevation_value = DecimalField(
        'Elevation',
        default=0.0,
        places=2,
        validators=[NumberRange(min=0.0)],
        description='Height above mean sea level',
    )
    elevation_unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=[('m', 'm')],
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[DataRequired()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsAccountBalanceForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.account_balance.value',
        unit_sel='sensors.account_balance.unit',
        location='sensors.account_balance.location',
        name='sensors.account_balance.name',
        description='sensors.account_balance.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Account balance')
    unit_sel = SelectField(
        'Unit',
        coerce=str,
        choices=SpaceEditSensorsForm._currency_choices(),
        validators=[DataRequired()],
        description='The unit of the sensor value',
    )
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsTotalMemberCountForm(SpaceEditSensorsForm):
    KEYS = dict(
        sensor_sel='sensors.total_member_count.value',
        location='sensors.total_member_count.location',
        name='sensors.total_member_count.name',
        description='sensors.total_member_count.description',
    )
    SENSORS = ['sensor_sel']

    sensor_sel = SpaceEditSensorsForm._sensor_field('Total member count')
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceEditSensorsNetworkTrafficForm(SpaceEditSensorsForm):
    KEYS = dict(
        bps_sensor_sel=(
            'sensors.network_traffic.properties.bits_per_second.value'
        ),
        bps_maximum=(
            'sensors.network_traffic.properties.bits_per_second.maximum'
        ),
        pps_sensor_sel=(
            'sensors.network_traffic.properties.packets_per_second.value'
        ),
        location='sensors.network_traffic.location',
        name='sensors.network_traffic.name',
        description='sensors.network_traffic.description',
    )
    SENSORS = [
        'bps_sensor_sel',
        'pps_sensor_sel',
    ]

    bps_sensor_sel = SpaceEditSensorsForm._sensor_field('Bits per second')
    bps_maximum = DecimalField(
        'Maximum bits per second',
        default=0.0,
        places=4,
        validators=[NumberRange(min=0.0)],
        description='E.g. as sold by your ISP',
    )
    pps_sensor_sel = SpaceEditSensorsForm._sensor_field('Packages per second')
    location = StringField(
        'Location',
        validators=[Optional()],
        description='The location of your sensor',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Give your sensor a name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='Some additional information',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )
