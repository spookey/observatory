from flask import current_app, url_for
from pytest import mark

from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def page_data(endpoint, *, url, keys):
    def res():
        pass

    res.endpoint = endpoint
    res.url = url
    res.keys = keys

    return res


PAGES = [
    page_data(
        'sapi.drop_cam',
        url='/space/drop/cam',
        keys=['cam'],
    ),
    page_data(
        'sapi.drop_contact_keymasters',
        url='/space/drop/contact/keymasters',
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
    page_data(
        'sapi.drop_sensors_temperature',
        url='/space/drop/sensors/temperature',
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
    page_data(
        'sapi.drop_sensors_door_locked',
        url='/space/drop/sensors/door-locked',
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
    page_data(
        'sapi.drop_sensors_barometer',
        url='/space/drop/sensors/barometer',
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
    page_data(
        'sapi.drop_sensors_humidity',
        url='/space/drop/sensors/humidity',
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
    page_data(
        'sapi.drop_sensors_beverage_supply',
        url='/space/drop/sensors/beverage-supply',
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
    page_data(
        'sapi.drop_projects',
        url='/space/drop/projects',
        keys=['projects'],
    ),
    page_data(
        'sapi.drop_links',
        url='/space/drop/links',
        keys=[
            'links.name',
            'links.description',
            'links.url',
        ],
    ),
    page_data(
        'sapi.drop_membership_plans',
        url='/space/drop/plans',
        keys=[
            'membership_plans.name',
            'membership_plans.value',
            'membership_plans.currency',
            'membership_plans.billing_interval',
            'membership_plans.description',
        ],
    ),
]
IDS = [page.endpoint.split('.')[-1] for page in PAGES]


@mark.usefixtures('session')
class TestSapiDropCommons:
    @staticmethod
    @mark.usefixtures('ctx_app')
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_urls(page):
        assert url_for(page.endpoint, idx=42) == f'{page.url}/42'

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_no_user(page, visitor):
        visitor(page.endpoint, params={'idx': 23}, method='post', code=401)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_disabled(page, monkeypatch, visitor, gen_user_loggedin):
        gen_user_loggedin()
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)

        visitor(page.endpoint, params={'idx': 42}, method='post', code=404)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_redirects(page, visitor, gen_user_loggedin):
        gen_user_loggedin()
        index_url = url_for('sapi.index', _external=True)

        res = visitor(
            page.endpoint, params={'idx': 23}, method='post', code=302
        )

        assert res.request.headers['LOCATION'] == index_url

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_deletes(page, visitor, gen_user_loggedin):
        gen_user_loggedin()

        idx = 5
        elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}', idx=idx, elem=f'{key} #{idx}'
            )
            for key in page.keys
        ]

        assert Value.query.all() == elems

        visitor(page.endpoint, params={'idx': idx}, method='post', code=302)

        assert Value.query.all() == []
