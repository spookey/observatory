from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_edit import (
    SpaceEditCamForm,
    SpaceEditContactForm,
    SpaceEditContactKeymastersForm,
    SpaceEditFeedBlogForm,
    SpaceEditFeedCalendarForm,
    SpaceEditFeedFlickrForm,
    SpaceEditFeedWikiForm,
    SpaceEditInfoForm,
    SpaceEditLinksForm,
    SpaceEditLocationForm,
    SpaceEditMembershipPlansForm,
    SpaceEditProjectsForm,
    SpaceEditSpaceFedForm,
    SpaceEditStateIconForm,
)
from observatory.forms.space_edit_sensors import (
    SpaceEditSensorsAccountBalanceForm,
    SpaceEditSensorsBarometerForm,
    SpaceEditSensorsBeverageSupplyForm,
    SpaceEditSensorsDoorLockedForm,
    SpaceEditSensorsHumidityForm,
    SpaceEditSensorsNetworkTrafficForm,
    SpaceEditSensorsPowerConsumptionForm,
    SpaceEditSensorsRadiationAlphaForm,
    SpaceEditSensorsRadiationBetaForm,
    SpaceEditSensorsRadiationBetaGammaForm,
    SpaceEditSensorsRadiationGammaForm,
    SpaceEditSensorsTemperatureForm,
    SpaceEditSensorsTotalMemberCountForm,
    SpaceEditSensorsWindForm,
)
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def form_edit(form, *, keys, data, one_of=None, sensors=None, **kwargs):
    def res():
        pass

    res.form = form
    res.data = data
    res.keys = keys
    res.one_of = one_of if one_of is not None else []
    res.sensors = sensors if sensors is not None else []
    res.empty = kwargs.get('empty', False)

    return res


FORMS = [
    form_edit(
        SpaceEditInfoForm,
        keys=dict(
            space='space',
            logo='logo',
            url='url',
        ),
        data=dict(
            space='some space',
            logo='https://example.org/logo.png',
            url='https://example.org',
        ),
    ),
    form_edit(
        SpaceEditLocationForm,
        keys=dict(
            address='location.address',
            lat='location.lat',
            lon='location.lon',
            timezone_sel='location.timezone',
        ),
        data=dict(
            address='somewhere',
            lat=23.5,
            lon=13.37,
            timezone_sel='UTC',
        ),
    ),
    form_edit(
        SpaceEditSpaceFedForm,
        keys=dict(
            spacenet='spacefed.spacenet',
            spacesaml='spacefed.spacesaml',
        ),
        data=dict(
            spacenet=True,
            spacesaml=False,
        ),
        empty=True,
    ),
    form_edit(
        SpaceEditCamForm,
        keys=dict(cam='cam'),
        data=dict(cam='https://example.org/webcam.mjpeg'),
    ),
    form_edit(
        SpaceEditStateIconForm,
        keys=dict(
            opened='state.icon.open',
            closed='state.icon.closed',
        ),
        data=dict(
            opened='https://example.org/open.png',
            closed='https://example.org/closed.png',
        ),
    ),
    form_edit(
        SpaceEditContactForm,
        keys=dict(
            phone='contact.phone',
            sip='contact.sip',
            irc='contact.irc',
            twitter='contact.twitter',
            mastodon='contact.mastodon',
            facebook='contact.facebook',
            identica='contact.identica',
            foursquare='contact.foursquare',
            email='contact.email',
            mailinglist='contact.ml',
            xmpp='contact.xmpp',
            issue_mail='contact.issue_mail',
            gopher='contact.gopher',
            matrix='contact.matrix',
            mumble='contact.mumble',
        ),
        data=dict(
            phone='+1 234 567 890',
            sip='sip:space@sip.example.org',
            irc='irc://example.org/#space',
            twitter='@space',
            mastodon='@space@example.net',
            facebook='https://example.com/space',
            identica='space@example.org',
            foursquare='000000000000000000000000',
            email='space@example.org',
            mailinglist='list@example.org',
            xmpp='chat@conference.example.org',
            issue_mail='space@example.org',
            gopher='gopher://gopher.space.example.org',
            matrix='#chat:example.org',
            mumble='mumble://mumble.example.org/space?version=0.0.1',
        ),
        one_of=['email', 'issue_mail', 'twitter', 'mailinglist'],
    ),
    form_edit(
        SpaceEditContactKeymastersForm,
        keys=dict(
            name='contact.keymasters.name',
            irc_nick='contact.keymasters.irc_nick',
            phone='contact.keymasters.phone',
            email='contact.keymasters.email',
            twitter='contact.keymasters.twitter',
            xmpp='contact.keymasters.xmpp',
            mastodon='contact.keymasters.mastodon',
            matrix='contact.keymasters.matrix',
        ),
        data=dict(
            name='somebody',
            irc_nick='somebody',
            phone='+1 234 567 890',
            email='somebody@example.org',
            twitter='@somebody',
            xmpp='somebody@chat.example.org',
            mastodon='@somebody@example.org',
            matrix='@somebody:matrix.example.org',
        ),
        one_of=[
            'irc_nick',
            'phone',
            'email',
            'twitter',
        ],
    ),
    form_edit(
        SpaceEditSensorsTemperatureForm,
        keys=dict(
            sensor_sel='sensors.temperature.value',
            elevate='sensors.temperature.value.elevate',
            convert_sel='sensors.temperature.value.convert',
            horizon_sel='sensors.temperature.value.horizon',
            unit_sel='sensors.temperature.unit',
            location='sensors.temperature.location',
            name='sensors.temperature.name',
            description='sensors.temperature.description',
        ),
        data=dict(
            sensor_sel=2,
            elevate=1.01,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='°C',
            location='somewhere',
            name='temperature sensor',
            description='measures the temperature',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsDoorLockedForm,
        keys=dict(
            sensor_sel='sensors.door_locked.value',
            elevate='sensors.door_locked.value.elevate',
            convert_sel='sensors.door_locked.value.convert',
            horizon_sel='sensors.door_locked.value.horizon',
            location='sensors.door_locked.location',
            name='sensors.door_locked.name',
            description='sensors.door_locked.description',
        ),
        data=dict(
            sensor_sel=5,
            elevate=1,
            convert_sel='BOOLEAN',
            horizon_sel='NORMAL',
            location='door',
            name='entry',
            description='our door',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsBarometerForm,
        keys=dict(
            sensor_sel='sensors.barometer.value',
            elevate='sensors.barometer.value.elevate',
            convert_sel='sensors.barometer.value.convert',
            horizon_sel='sensors.barometer.value.horizon',
            unit_sel='sensors.barometer.unit',
            location='sensors.barometer.location',
            name='sensors.barometer.name',
            description='sensors.barometer.description',
        ),
        data=dict(
            sensor_sel=7,
            elevate=1,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='hPa',
            location='somewhere',
            name='barometer',
            description='measures the weather',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsRadiationAlphaForm,
        keys=dict(
            sensor_sel='sensors.radiation.alpha.value',
            elevate='sensors.radiation.alpha.value.elevate',
            convert_sel='sensors.radiation.alpha.value.convert',
            horizon_sel='sensors.radiation.alpha.value.horizon',
            unit_sel='sensors.radiation.alpha.unit',
            dead_time='sensors.radiation.alpha.dead_time',
            conversion_factor='sensors.radiation.alpha.conversion_factor',
            location='sensors.radiation.alpha.location',
            name='sensors.radiation.alpha.name',
            description='sensors.radiation.alpha.description',
        ),
        data=dict(
            sensor_sel=1,
            elevate=1.0,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='alpha sensor',
            description='measures alpha radiation',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsRadiationBetaForm,
        keys=dict(
            sensor_sel='sensors.radiation.beta.value',
            elevate='sensors.radiation.beta.value.elevate',
            convert_sel='sensors.radiation.beta.value.convert',
            horizon_sel='sensors.radiation.beta.value.horizon',
            unit_sel='sensors.radiation.beta.unit',
            dead_time='sensors.radiation.beta.dead_time',
            conversion_factor='sensors.radiation.beta.conversion_factor',
            location='sensors.radiation.beta.location',
            name='sensors.radiation.beta.name',
            description='sensors.radiation.beta.description',
        ),
        data=dict(
            sensor_sel=1,
            elevate=1.0,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='beta sensor',
            description='measures beta radiation',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsRadiationGammaForm,
        keys=dict(
            sensor_sel='sensors.radiation.gamma.value',
            elevate='sensors.radiation.gamma.value.elevate',
            convert_sel='sensors.radiation.gamma.value.convert',
            horizon_sel='sensors.radiation.gamma.value.horizon',
            unit_sel='sensors.radiation.gamma.unit',
            dead_time='sensors.radiation.gamma.dead_time',
            conversion_factor='sensors.radiation.gamma.conversion_factor',
            location='sensors.radiation.gamma.location',
            name='sensors.radiation.gamma.name',
            description='sensors.radiation.gamma.description',
        ),
        data=dict(
            sensor_sel=1,
            elevate=1.0,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='gamma sensor',
            description='measures gamma radiation',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsRadiationBetaGammaForm,
        keys=dict(
            sensor_sel='sensors.radiation.beta_gamma.value',
            elevate='sensors.radiation.beta_gamma.value.elevate',
            convert_sel='sensors.radiation.beta_gamma.value.convert',
            horizon_sel='sensors.radiation.beta_gamma.value.horizon',
            unit_sel='sensors.radiation.beta_gamma.unit',
            dead_time='sensors.radiation.beta_gamma.dead_time',
            conversion_factor='sensors.radiation.beta_gamma.conversion_factor',
            location='sensors.radiation.beta_gamma.location',
            name='sensors.radiation.beta_gamma.name',
            description='sensors.radiation.beta_gamma.description',
        ),
        data=dict(
            sensor_sel=1,
            elevate=1.0,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='beta_gamma sensor',
            description='measures beta and gamma radiation',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsHumidityForm,
        keys=dict(
            sensor_sel='sensors.humidity.value',
            elevate='sensors.humidity.value.elevate',
            convert_sel='sensors.humidity.value.convert',
            horizon_sel='sensors.humidity.value.horizon',
            unit_sel='sensors.humidity.unit',
            location='sensors.humidity.location',
            name='sensors.humidity.name',
            description='sensors.humidity.description',
        ),
        data=dict(
            sensor_sel=3,
            elevate=1,
            convert_sel='INTEGER',
            horizon_sel='NORMAL',
            unit_sel='%',
            location='somewhere',
            name='humidity',
            description='wet',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsBeverageSupplyForm,
        keys=dict(
            sensor_sel='sensors.beverage_supply.value',
            elevate='sensors.beverage_supply.value.elevate',
            convert_sel='sensors.beverage_supply.value.convert',
            horizon_sel='sensors.beverage_supply.value.horizon',
            unit_sel='sensors.beverage_supply.unit',
            location='sensors.beverage_supply.location',
            name='sensors.beverage_supply.name',
            description='sensors.beverage_supply.description',
        ),
        data=dict(
            sensor_sel=6,
            elevate=1,
            convert_sel='INTEGER',
            horizon_sel='NORMAL',
            unit_sel='crt',
            location='somewhere',
            name='drinks',
            description='nice',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsPowerConsumptionForm,
        keys=dict(
            sensor_sel='sensors.power_consumption.value',
            elevate='sensors.power_consumption.value.elevate',
            convert_sel='sensors.power_consumption.value.convert',
            horizon_sel='sensors.power_consumption.value.horizon',
            unit_sel='sensors.power_consumption.unit',
            location='sensors.power_consumption.location',
            name='sensors.power_consumption.name',
            description='sensors.power_consumption.description',
        ),
        data=dict(
            sensor_sel=5,
            elevate=99,
            convert_sel='NATURAL',
            horizon_sel='INVERT',
            unit_sel='W',
            location='cellar',
            name='power',
            description='electronic deluxe',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsWindForm,
        keys=dict(
            speed_sensor_sel='sensors.wind.properties.speed.value',
            speed_elevate='sensors.wind.properties.speed.value.elevate',
            speed_convert_sel='sensors.wind.properties.speed.value.convert',
            speed_horizon_sel='sensors.wind.properties.speed.value.horizon',
            speed_unit_sel='sensors.wind.properties.speed.unit',
            gust_sensor_sel='sensors.wind.properties.gust.value',
            gust_elevate='sensors.wind.properties.gust.value.elevate',
            gust_convert_sel='sensors.wind.properties.gust.value.convert',
            gust_horizon_sel='sensors.wind.properties.gust.value.horizon',
            gust_unit_sel='sensors.wind.properties.gust.unit',
            direction_sensor_sel='sensors.wind.properties.direction.value',
            direction_elevate=(
                'sensors.wind.properties.direction.value.elevate'
            ),
            direction_convert_sel=(
                'sensors.wind.properties.direction.value.convert'
            ),
            direction_horizon_sel=(
                'sensors.wind.properties.direction.value.horizon'
            ),
            direction_unit_sel=('sensors.wind.properties.direction.unit'),
            elevation_sensor_sel='sensors.wind.properties.elevation.value',
            elevation_elevate=(
                'sensors.wind.properties.elevation.value.elevate'
            ),
            elevation_convert_sel=(
                'sensors.wind.properties.elevation.value.convert'
            ),
            elevation_horizon_sel=(
                'sensors.wind.properties.elevation.value.horizon'
            ),
            elevation_unit_sel='sensors.wind.properties.elevation.unit',
            location='sensors.wind.location',
            name='sensors.wind.name',
            description='sensors.wind.description',
        ),
        data=dict(
            speed_sensor_sel=1,
            speed_elevate=1.1,
            speed_convert_sel='NATURAL',
            speed_horizon_sel='NORMAL',
            speed_unit_sel='m/s',
            gust_sensor_sel=3,
            gust_elevate=1.3,
            gust_convert_sel='NATURAL',
            gust_horizon_sel='NORMAL',
            gust_unit_sel='m/s',
            direction_sensor_sel=5,
            direction_elevate=1.5,
            direction_convert_sel='INTEGER',
            direction_horizon_sel='NORMAL',
            direction_unit_sel='°',
            elevation_sensor_sel=7,
            elevation_elevate=1.7,
            elevation_convert_sel='INTEGER',
            elevation_horizon_sel='NORMAL',
            elevation_unit_sel='m',
            location='roof',
            name='wind sensor',
            description='windy',
        ),
        sensors=[
            'speed_sensor_sel',
            'gust_sensor_sel',
            'direction_sensor_sel',
            'elevation_sensor_sel',
        ],
    ),
    form_edit(
        SpaceEditSensorsAccountBalanceForm,
        keys=dict(
            sensor_sel='sensors.account_balance.value',
            elevate='sensors.account_balance.value.elevate',
            convert_sel='sensors.account_balance.value.convert',
            horizon_sel='sensors.account_balance.value.horizon',
            unit_sel='sensors.account_balance.unit',
            location='sensors.account_balance.location',
            name='sensors.account_balance.name',
            description='sensors.account_balance.description',
        ),
        data=dict(
            sensor_sel=7,
            elevate=1.0001,
            convert_sel='NATURAL',
            horizon_sel='INVERT',
            unit_sel='RUB',
            location='in your pocked',
            name='cash',
            description='moneu',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsTotalMemberCountForm,
        keys=dict(
            sensor_sel='sensors.total_member_count.value',
            elevate='sensors.total_member_count.value.elevate',
            convert_sel='sensors.total_member_count.value.convert',
            horizon_sel='sensors.total_member_count.value.horizon',
            location='sensors.total_member_count.location',
            name='sensors.total_member_count.name',
            description='sensors.total_member_count.description',
        ),
        data=dict(
            sensor_sel=8,
            elevate=1.0,
            convert_sel='INTEGER',
            horizon_sel='INVERT',
            location='space',
            name='total',
            description='how many',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditSensorsNetworkTrafficForm,
        keys=dict(
            bps_sensor_sel=(
                'sensors.network_traffic.properties.bits_per_second.value'
            ),
            bps_elevate=(
                'sensors.network_traffic.properties.'
                'bits_per_second.value.elevate'
            ),
            bps_convert_sel=(
                'sensors.network_traffic.properties.'
                'bits_per_second.value.convert'
            ),
            bps_horizon_sel=(
                'sensors.network_traffic.properties.'
                'bits_per_second.value.horizon'
            ),
            bps_maximum=(
                'sensors.network_traffic.properties.bits_per_second.maximum'
            ),
            pps_sensor_sel=(
                'sensors.network_traffic.properties.packets_per_second.value'
            ),
            pps_elevate=(
                'sensors.network_traffic.properties.'
                'packets_per_second.value.elevate'
            ),
            pps_convert_sel=(
                'sensors.network_traffic.properties.'
                'packets_per_second.value.convert'
            ),
            pps_horizon_sel=(
                'sensors.network_traffic.properties.'
                'packets_per_second.value.horizon'
            ),
            location='sensors.network_traffic.location',
            name='sensors.network_traffic.name',
            description='sensors.network_traffic.description',
        ),
        data=dict(
            bps_sensor_sel=1,
            bps_elevate=1.1,
            bps_convert_sel='INTEGER',
            bps_horizon_sel='NORMAL',
            bps_maximum=13.37,
            pps_sensor_sel=3,
            pps_elevate=1.3,
            pps_convert_sel='INTEGER',
            pps_horizon_sel='NORMAL',
            location='router',
            name='network traffic',
            description='our network is networking',
        ),
        sensors=[
            'bps_sensor_sel',
            'pps_sensor_sel',
        ],
    ),
    form_edit(
        SpaceEditFeedBlogForm,
        keys=dict(
            type_sel='feeds.blog.type',
            url='feeds.blog.url',
        ),
        data=dict(
            type_sel='atom',
            url='https://blog.example.org/feed',
        ),
    ),
    form_edit(
        SpaceEditFeedWikiForm,
        keys=dict(
            type_sel='feeds.wiki.type',
            url='feeds.wiki.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://wiki.example.org/feed.xml',
        ),
    ),
    form_edit(
        SpaceEditFeedCalendarForm,
        keys=dict(
            type_sel='feeds.calendar.type',
            url='feeds.calendar.url',
        ),
        data=dict(
            type_sel='ical',
            url='https://calendar.example.org/ical',
        ),
    ),
    form_edit(
        SpaceEditFeedFlickrForm,
        keys=dict(
            type_sel='feeds.flickr.type',
            url='feeds.flickr.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://example.com/space/feed.rss',
        ),
    ),
    form_edit(
        SpaceEditProjectsForm,
        keys=dict(projects='projects'),
        data=dict(projects='https://project.example.org/'),
    ),
    form_edit(
        SpaceEditLinksForm,
        keys=dict(
            name='links.name',
            description='links.description',
            url='links.url',
        ),
        data=dict(
            name='some link',
            description='This is just a link',
            url='https://example.org',
        ),
    ),
    form_edit(
        SpaceEditMembershipPlansForm,
        keys=dict(
            name='membership_plans.name',
            value='membership_plans.value',
            currency_sel='membership_plans.currency',
            billing_interval_sel='membership_plans.billing_interval',
            description='membership_plans.description',
        ),
        data=dict(
            name='gold plan',
            value=23.5,
            currency_sel='XAU',
            billing_interval_sel='hourly',
            description='please pay',
        ),
    ),
]
IDS = [edit.form.__name__ for edit in FORMS]


@mark.usefixtures('session', 'ctx_app')
class TestSpaceEditCommons:
    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_meta(edit):
        keys = edit.keys.keys()
        assert sorted(keys) == sorted(edit.data.keys())
        for key in edit.one_of:
            assert key in keys

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_keys(edit):
        assert edit.form.KEYS == edit.keys

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_one_of(edit):
        assert edit.form.ONE_OF == edit.one_of

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_form_idx(edit):
        idx = choice(range(23, 42))
        form = edit.form(idx=idx)
        assert form.idx == idx

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_basic_fields(edit):
        form = edit.form(idx=0)
        for field in edit.keys.keys():
            elem = getattr(form, field, 'error')
            assert elem is not None
            assert elem != 'error'
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_submit_button(edit):
        form = edit.form(idx=0)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_submit'

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_empty_invalid(edit):
        form = edit.form(idx=0)
        assert form.validate() is edit.empty
        action = form.action()
        if edit.empty:
            assert action is not None
        else:
            assert action is None

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_create_new(edit, gen_sensor):
        assert Value.query.all() == []

        sensors = {
            name: gen_sensor(name, prime=edit.data[name])
            for name in edit.sensors
        }

        form = edit.form(idx=0, **edit.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in edit.keys.items():
            val = Value.get(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            base = sensors if form_key in edit.sensors else edit.data

            assert val == base.get(form_key, 'error')

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_change_existing(edit, gen_sensor):
        assert Value.query.all() == []

        sensors = {
            name: gen_sensor(name, prime=edit.data[name])
            for name in edit.sensors
        }

        for form_key, space_key in edit.keys.items():
            old_value = edit.data.get(form_key, 'some')

            if isinstance(old_value, bool):
                old_value = not old_value
            else:
                old_value = 2 * old_value

            if form_key in edit.sensors:
                old_value = gen_sensor(f'old_{form_key}', prime=old_value)

            Value.set(
                key=f'{SP_API_PREFIX}.{space_key}', idx=0, elem=old_value
            )

        assert Value.query.all() != []

        form = edit.form(idx=0, **edit.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in edit.keys.items():
            val = Value.get(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            base = sensors if form_key in edit.sensors else edit.data

            assert val == base.get(form_key, 'error')
