from flask import current_app, url_for
from pytest import mark

from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def page_data(endpoint, *, url, keys, data, sensors=None, **kwargs):
    def res():
        pass

    res.endpoint = endpoint
    res.url = url
    res.keys = keys
    res.data = data
    res.sensors = sensors if sensors is not None else []
    res.multi = kwargs.get('multi', False)

    return res


PAGES = [
    page_data(
        'sapi.edit_info',
        url='/space/edit/info',
        keys=dict(
            space='space',
            logo='logo',
            url='url',
        ),
        data=dict(
            space='space',
            logo='https://example.org/logo.png',
            url='https://example.org',
        ),
    ),
    page_data(
        'sapi.edit_location',
        url='/space/edit/location',
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
    page_data(
        'sapi.edit_spacefed',
        url='/space/edit/spacefed',
        keys=dict(
            spacenet='spacefed.spacenet',
            spacesaml='spacefed.spacesaml',
        ),
        data=dict(
            spacenet=True,
            spacesaml=True,
        ),
    ),
    page_data(
        'sapi.edit_cam',
        url='/space/edit/cam',
        keys=dict(cam='cam'),
        data=dict(cam='https://example.org/webcam'),
        multi=True,
    ),
    page_data(
        'sapi.edit_state_icon',
        url='/space/edit/state/icon',
        keys=dict(
            opened='state.icon.open',
            closed='state.icon.closed',
        ),
        data=dict(
            opened='https://example.org/open.png',
            closed='https://example.org/closed.png',
        ),
    ),
    page_data(
        'sapi.edit_contact',
        url='/space/edit/contact',
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
    ),
    page_data(
        'sapi.edit_contact_keymasters',
        url='/space/edit/contact/keymasters',
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
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_temperature',
        url='/space/edit/sensors/temperature',
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
            elevate=1.5,
            convert_sel='NATURAL',
            horizon_sel='NORMAL',
            unit_sel='K',
            location='upstairs',
            name='temperature',
            description='temperature sensor',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_door_locked',
        url='/space/edit/sensors/door-locked',
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
            location='entry',
            name='main door',
            description='the door where you can go in',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_barometer',
        url='/space/edit/sensors/barometer',
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
            sensor_sel=6,
            elevate=1,
            convert_sel='NATURAL',
            horizon_sel='INVERT',
            unit_sel='hPA',
            location='downstairs',
            name='barometer',
            description='our barometer',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_humidity',
        url='/space/edit/sensors/humidity',
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
            location='upstairs',
            name='humidity',
            description='our humidity sensor',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_beverage_supply',
        url='/space/edit/sensors/beverage-supply',
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
            sensor_sel=7,
            elevate=1,
            convert_sel='INTEGER',
            horizon_sel='NORMAL',
            unit_sel='crt',
            location='cellar',
            name='beer',
            description='yes',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_power_consumption',
        url='/space/edit/sensors/power-consumption',
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
            sensor_sel=8,
            elevate=9,
            convert_sel='NATURAL',
            horizon_sel='INVERT',
            unit_sel='W',
            location='cellar',
            name='power',
            description='electricity',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_wind',
        url='/space/edit/sensors/wind',
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
            direction_unit_sel='sensors.wind.properties.direction.unit',
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
            speed_sensor_sel=2,
            speed_elevate=1.2,
            speed_convert_sel='NATURAL',
            speed_horizon_sel='NORMAL',
            speed_unit_sel='m/s',
            gust_sensor_sel=4,
            gust_elevate=1.4,
            gust_convert_sel='NATURAL',
            gust_horizon_sel='NORMAL',
            gust_unit_sel='m/s',
            direction_sensor_sel=6,
            direction_elevate=1.6,
            direction_convert_sel='INTEGER',
            direction_horizon_sel='NORMAL',
            direction_unit_sel='°',
            elevation_sensor_sel=8,
            elevation_elevate=1.8,
            elevation_convert_sel='INTEGER',
            elevation_horizon_sel='NORMAL',
            elevation_unit_sel='m',
            location='outside',
            name='wind sensor',
            description='windy',
        ),
        sensors=[
            'speed_sensor_sel',
            'gust_sensor_sel',
            'direction_sensor_sel',
            'elevation_sensor_sel',
        ],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_account_balance',
        url='/space/edit/sensors/account-balance',
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
            sensor_sel=3,
            elevate=0.99999,
            convert_sel='NATURAL',
            horizon_sel='INVERT',
            unit_sel='EUR',
            location='pocket',
            name='cash',
            description='money',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_total_member_count',
        url='/space/edit/sensors/total-member-count',
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
            sensor_sel=6,
            elevate=1.0,
            convert_sel='INTEGER',
            horizon_sel='NORMAL',
            location='space',
            name='member',
            description='count',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_feeds_blog',
        url='/space/edit/feeds/blog',
        keys=dict(
            type_sel='feeds.blog.type',
            url='feeds.blog.url',
        ),
        data=dict(
            type_sel='atom',
            url='https://blog.example.org/feed',
        ),
    ),
    page_data(
        'sapi.edit_feeds_wiki',
        url='/space/edit/feeds/wiki',
        keys=dict(
            type_sel='feeds.wiki.type',
            url='feeds.wiki.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://wiki.example.org/feed.xml',
        ),
    ),
    page_data(
        'sapi.edit_feeds_calendar',
        url='/space/edit/feeds/calendar',
        keys=dict(
            type_sel='feeds.calendar.type',
            url='feeds.calendar.url',
        ),
        data=dict(
            type_sel='ical',
            url='https://calendar.example.org/ical',
        ),
    ),
    page_data(
        'sapi.edit_feeds_flickr',
        url='/space/edit/feeds/flickr',
        keys=dict(
            type_sel='feeds.flickr.type',
            url='feeds.flickr.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://example.com/space/feed.rss',
        ),
    ),
    page_data(
        'sapi.edit_projects',
        url='/space/edit/projects',
        keys=dict(projects='projects'),
        data=dict(projects='https://project.example.org/'),
        multi=True,
    ),
    page_data(
        'sapi.edit_links',
        url='/space/edit/links',
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
        multi=True,
    ),
    page_data(
        'sapi.edit_membership_plans',
        url='/space/edit/plans',
        keys=dict(
            name='membership_plans.name',
            value='membership_plans.value',
            currency_sel='membership_plans.currency',
            billing_interval_sel='membership_plans.billing_interval',
            description='membership_plans.description',
        ),
        data=dict(
            name='silver plan',
            value=42.0,
            currency_sel='XAG',
            billing_interval_sel='hourly',
            description='please pay',
        ),
        multi=True,
    ),
]
IDS = [page.endpoint.split('.')[-1] for page in PAGES]


@mark.usefixtures('session')
class TestSapiEditCommons:
    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_page_page(page):
        assert sorted(page.keys.keys()) == sorted(page.data.keys())

    @staticmethod
    @mark.usefixtures('ctx_app')
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_urls(page):
        assert url_for(page.endpoint) == page.url
        if page.multi:
            assert url_for(page.endpoint, idx=23) == f'{page.url}/23'

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_no_user(page, visitor):
        visitor(page.endpoint, code=401)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_disabled(page, monkeypatch, visitor, gen_user_loggedin):
        gen_user_loggedin()
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)

        visitor(page.endpoint, code=404)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_params(page, visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(page.endpoint)

        form = res.soup.select('form')[-1]
        assert form['method'] == 'POST'
        assert form['action'] == url_for(page.endpoint, _external=True)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_creates(page, visitor, gen_user_loggedin, gen_sensor):
        gen_user_loggedin()
        index_url = url_for('sapi.index', _external=True)

        assert Value.query.all() == []

        sensors = {
            name: gen_sensor(name, prime=page.data[name])
            for name in page.sensors
        }

        res = visitor(
            page.endpoint,
            method='post',
            data={**page.data, 'submit': True},
            code=302,
        )

        assert res.request.headers['LOCATION'] == index_url
        for form_key, space_key in page.keys.items():
            val = Value.get(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            base = sensors if form_key in page.sensors else page.data

            assert val == base.get(form_key, 'error')
