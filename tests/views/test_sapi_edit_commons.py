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
            unit_sel='sensors.temperature.unit',
            location='sensors.temperature.location',
            name='sensors.temperature.name',
            description='sensors.temperature.description',
        ),
        data=dict(
            sensor_sel=2,
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
            location='sensors.door_locked.location',
            name='sensors.door_locked.name',
            description='sensors.door_locked.description',
        ),
        data=dict(
            sensor_sel=5,
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
            unit_sel='sensors.barometer.unit',
            location='sensors.barometer.location',
            name='sensors.barometer.name',
            description='sensors.barometer.description',
        ),
        data=dict(
            sensor_sel=6,
            unit_sel='hPA',
            location='downstairs',
            name='barometer',
            description='our barometer',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_radiation_alpha',
        url='/space/edit/sensors/radiation/alpha',
        keys=dict(
            sensor_sel='sensors.radiation.alpha.value',
            unit_sel='sensors.radiation.alpha.unit',
            dead_time='sensors.radiation.alpha.dead_time',
            conversion_factor='sensors.radiation.alpha.conversion_factor',
            location='sensors.radiation.alpha.location',
            name='sensors.radiation.alpha.name',
            description='sensors.radiation.alpha.description',
        ),
        data=dict(
            sensor_sel=1,
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='alpha sensor',
            description='measures alpha radiation',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_radiation_beta',
        url='/space/edit/sensors/radiation/beta',
        keys=dict(
            sensor_sel='sensors.radiation.beta.value',
            unit_sel='sensors.radiation.beta.unit',
            dead_time='sensors.radiation.beta.dead_time',
            conversion_factor='sensors.radiation.beta.conversion_factor',
            location='sensors.radiation.beta.location',
            name='sensors.radiation.beta.name',
            description='sensors.radiation.beta.description',
        ),
        data=dict(
            sensor_sel=1,
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='beta sensor',
            description='measures beta radiation',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_radiation_gamma',
        url='/space/edit/sensors/radiation/gamma',
        keys=dict(
            sensor_sel='sensors.radiation.gamma.value',
            unit_sel='sensors.radiation.gamma.unit',
            dead_time='sensors.radiation.gamma.dead_time',
            conversion_factor='sensors.radiation.gamma.conversion_factor',
            location='sensors.radiation.gamma.location',
            name='sensors.radiation.gamma.name',
            description='sensors.radiation.gamma.description',
        ),
        data=dict(
            sensor_sel=1,
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='gamma sensor',
            description='measures gamma radiation',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_radiation_beta_gamma',
        url='/space/edit/sensors/radiation/beta-gamma',
        keys=dict(
            sensor_sel='sensors.radiation.beta_gamma.value',
            unit_sel='sensors.radiation.beta_gamma.unit',
            dead_time='sensors.radiation.beta_gamma.dead_time',
            conversion_factor='sensors.radiation.beta_gamma.conversion_factor',
            location='sensors.radiation.beta_gamma.location',
            name='sensors.radiation.beta_gamma.name',
            description='sensors.radiation.beta_gamma.description',
        ),
        data=dict(
            sensor_sel=1,
            unit_sel='cpm',
            dead_time=1.0,
            conversion_factor=1.0,
            location='roof',
            name='beta_gamma sensor',
            description='measures beta and gamma radiation',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_humidity',
        url='/space/edit/sensors/humidity',
        keys=dict(
            sensor_sel='sensors.humidity.value',
            unit_sel='sensors.humidity.unit',
            location='sensors.humidity.location',
            name='sensors.humidity.name',
            description='sensors.humidity.description',
        ),
        data=dict(
            sensor_sel=3,
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
            unit_sel='sensors.beverage_supply.unit',
            location='sensors.beverage_supply.location',
            name='sensors.beverage_supply.name',
            description='sensors.beverage_supply.description',
        ),
        data=dict(
            sensor_sel=7,
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
            unit_sel='sensors.power_consumption.unit',
            location='sensors.power_consumption.location',
            name='sensors.power_consumption.name',
            description='sensors.power_consumption.description',
        ),
        data=dict(
            sensor_sel=8,
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
        ),
        data=dict(
            speed_sensor_sel=2,
            speed_unit_sel='m/s',
            gust_sensor_sel=4,
            gust_unit_sel='m/s',
            direction_sensor_sel=6,
            direction_unit_sel='°',
            elevation_value=321.0,
            elevation_unit_sel='m',
            location='outside',
            name='wind sensor',
            description='windy',
        ),
        sensors=[
            'speed_sensor_sel',
            'gust_sensor_sel',
            'direction_sensor_sel',
        ],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_account_balance',
        url='/space/edit/sensors/account-balance',
        keys=dict(
            sensor_sel='sensors.account_balance.value',
            unit_sel='sensors.account_balance.unit',
            location='sensors.account_balance.location',
            name='sensors.account_balance.name',
            description='sensors.account_balance.description',
        ),
        data=dict(
            sensor_sel=3,
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
            location='sensors.total_member_count.location',
            name='sensors.total_member_count.name',
            description='sensors.total_member_count.description',
        ),
        data=dict(
            sensor_sel=6,
            location='space',
            name='member',
            description='count',
        ),
        sensors=['sensor_sel'],
        multi=True,
    ),
    page_data(
        'sapi.edit_sensors_network_traffic',
        url='/space/edit/sensors/network-traffic',
        keys=dict(
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
        ),
        data=dict(
            bps_sensor_sel=2,
            bps_maximum=13.37,
            pps_sensor_sel=4,
            location='switch',
            name='traffic',
            description='collecting bits',
        ),
        sensors=[
            'bps_sensor_sel',
            'pps_sensor_sel',
        ],
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
