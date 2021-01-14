from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.mapper import EnumConvert, EnumHorizon
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiBuildValue:
    @staticmethod
    def test_api_compatibility():
        res = SpaceApi().build()
        assert res['api_compatibility'] == ['14']

    @staticmethod
    def test_space_logo_url():
        api = SpaceApi()
        space = Value.set(
            key=f'{SP_API_PREFIX}.space', idx=0, elem='space'
        ).elem
        logo = Value.set(
            key=f'{SP_API_PREFIX}.logo',
            idx=0,
            elem='https://example.org/image.gif',
        ).elem
        url = Value.set(
            key=f'{SP_API_PREFIX}.url', idx=0, elem='https://example.net'
        ).elem

        res = api.build()
        assert res['space'] == space
        assert res['logo'] == logo
        assert res['url'] == url

    @staticmethod
    def test_location():
        api = SpaceApi()
        address = Value.set(
            key=f'{SP_API_PREFIX}.location.address',
            idx=0,
            elem='Somewhere 23, 12345 FNORD',
        ).elem
        lat = Value.set(
            key=f'{SP_API_PREFIX}.location.lat', idx=0, elem=23.5
        ).elem
        lon = Value.set(
            key=f'{SP_API_PREFIX}.location.lon', idx=0, elem=133.7
        ).elem
        timezone = Value.set(
            key=f'{SP_API_PREFIX}.location.timezone', idx=0, elem='UTC'
        ).elem

        res = api.build()
        assert res['location']['address'] == address
        assert res['location']['lat'] == lat
        assert res['location']['lon'] == lon
        assert res['location']['timezone'] == timezone

    @staticmethod
    def test_spacefed():
        api = SpaceApi()
        spacenet = Value.set(
            key=f'{SP_API_PREFIX}.spacefed.spacenet', idx=0, elem=True
        ).elem
        spacesaml = Value.set(
            key=f'{SP_API_PREFIX}.spacefed.spacesaml', idx=0, elem=False
        ).elem

        res = api.build()
        assert res['spacefed']['spacenet'] == spacenet
        assert res['spacefed']['spacesaml'] == spacesaml

    @staticmethod
    def test_cam():
        api = SpaceApi()
        nil_cam = Value.set(
            key=f'{SP_API_PREFIX}.cam',
            idx=0,
            elem='https://example.org/cam.mjpg',
        ).elem
        two_cam = Value.set(
            key=f'{SP_API_PREFIX}.cam',
            idx=2,
            elem='https://example.com/webcam',
        ).elem

        res = api.build()
        assert res['cam'] == [
            {'_idx': 0, 'value': nil_cam},
            {'_idx': 2, 'value': two_cam},
        ]

    @staticmethod
    def test_contact_telephone():
        api = SpaceApi()
        phone = Value.set(
            key=f'{SP_API_PREFIX}.contact.phone', idx=0, elem='+1 234 567 890'
        ).elem
        sip = Value.set(
            key=f'{SP_API_PREFIX}.contact.sip',
            idx=0,
            elem='sip:space@sip.example.org',
        ).elem

        res = api.build()
        assert res['contact']['phone'] == phone
        assert res['contact']['sip'] == sip

    @staticmethod
    def test_contact_chats():
        api = SpaceApi()
        irc = Value.set(
            key=f'{SP_API_PREFIX}.contact.irc',
            idx=0,
            elem='irc://example.org/#space',
        ).elem
        xmpp = Value.set(
            key=f'{SP_API_PREFIX}.contact.xmpp',
            idx=0,
            elem='chat@conference.example.org',
        ).elem
        matrix = Value.set(
            key=f'{SP_API_PREFIX}.contact.matrix',
            idx=0,
            elem='#chat:example.org',
        ).elem
        mumble = Value.set(
            key=f'{SP_API_PREFIX}.contact.mumble',
            idx=0,
            elem='mumble://mumble.example.org/space?version=0.0.1',
        ).elem

        res = api.build()
        assert res['contact']['irc'] == irc
        assert res['contact']['xmpp'] == xmpp
        assert res['contact']['matrix'] == matrix
        assert res['contact']['mumble'] == mumble

    @staticmethod
    def test_contact_social():
        api = SpaceApi()
        twitter = Value.set(
            key=f'{SP_API_PREFIX}.contact.twitter', idx=0, elem='@space'
        ).elem
        mastodon = Value.set(
            key=f'{SP_API_PREFIX}.contact.mastodon',
            idx=0,
            elem='@space@example.net',
        ).elem
        facebook = Value.set(
            key=f'{SP_API_PREFIX}.contact.facebook',
            idx=0,
            elem='https://example.com/space',
        ).elem
        identica = Value.set(
            key=f'{SP_API_PREFIX}.contact.identica',
            idx=0,
            elem='space@example.org',
        ).elem

        res = api.build()
        assert res['contact']['twitter'] == twitter
        assert res['contact']['mastodon'] == mastodon
        assert res['contact']['facebook'] == facebook
        assert res['contact']['identica'] == identica

    @staticmethod
    def test_contact_network():
        api = SpaceApi()
        foursquare = Value.set(
            key=f'{SP_API_PREFIX}.contact.foursquare',
            idx=0,
            elem='000000000000000000000000',
        ).elem
        gopher = Value.set(
            key=f'{SP_API_PREFIX}.contact.gopher',
            idx=0,
            elem='gopher://gopher.space.example.org',
        ).elem

        res = api.build()
        assert res['contact']['foursquare'] == foursquare
        assert res['contact']['gopher'] == gopher

    @staticmethod
    def test_contact_mail():
        api = SpaceApi()
        email = Value.set(
            key=f'{SP_API_PREFIX}.contact.email',
            idx=0,
            elem='space@example.org',
        ).elem
        mailinglist = Value.set(
            key=f'{SP_API_PREFIX}.contact.ml', idx=0, elem='list@example.org'
        ).elem
        issue_mail = Value.set(
            key=f'{SP_API_PREFIX}.contact.issue_mail',
            idx=0,
            elem='space@example.org',
        ).elem

        res = api.build()
        assert res['contact']['email'] == email
        assert res['contact']['ml'] == mailinglist
        assert res['contact']['issue_mail'] == issue_mail

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=0, elem='nil'
        ).elem
        one_name = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=1, elem='one'
        ).elem
        Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=2, elem='two'
        )

        nil_phone = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.phone',
            idx=0,
            elem='+1 234 567 890',
        ).elem
        nil_email = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.email',
            idx=0,
            elem='nil@example.org',
        ).elem
        one_email = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.email',
            idx=1,
            elem='one@example.org',
        ).elem
        one_xmpp = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.xmpp',
            idx=1,
            elem='one@jabber.example.org',
        ).elem
        Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.xmpp',
            idx=2,
            elem='two@jabber.example.org',
        )

        res = api.build()
        assert res['contact']['keymasters'] == [
            {
                '_idx': 0,
                'name': nil_name,
                'irc_nick': None,
                'phone': nil_phone,
                'email': nil_email,
                'twitter': None,
                'xmpp': None,
                'matrix': None,
                'mastodon': None,
            },
            {
                '_idx': 1,
                'name': one_name,
                'irc_nick': None,
                'phone': None,
                'email': one_email,
                'twitter': None,
                'xmpp': one_xmpp,
                'matrix': None,
                'mastodon': None,
            },
        ]

    @staticmethod
    @mark.parametrize(
        ('field', 'sensors', 'fields'),
        [
            (
                'temperature',
                dict(value=('sensors.temperature.value', EnumConvert.NATURAL)),
                dict(
                    unit='sensors.temperature.unit',
                    location='sensors.temperature.location',
                    name='sensors.temperature.name',
                    description='sensors.temperature.description',
                ),
            ),
            (
                'door_locked',
                dict(value=('sensors.door_locked.value', EnumConvert.BOOLEAN)),
                dict(
                    location='sensors.door_locked.location',
                    name='sensors.door_locked.name',
                    description='sensors.door_locked.description',
                ),
            ),
            (
                'barometer',
                dict(value=('sensors.barometer.value', EnumConvert.NATURAL)),
                dict(
                    unit='sensors.barometer.unit',
                    location='sensors.barometer.location',
                    name='sensors.barometer.name',
                    description='sensors.barometer.description',
                ),
            ),
            (
                'humidity',
                dict(value=('sensors.humidity.value', EnumConvert.INTEGER)),
                dict(
                    unit='sensors.humidity.unit',
                    location='sensors.humidity.location',
                    name='sensors.humidity.name',
                    description='sensors.humidity.description',
                ),
            ),
            (
                'beverage_supply',
                dict(
                    value=(
                        'sensors.beverage_supply.value',
                        EnumConvert.INTEGER,
                    )
                ),
                dict(
                    unit='sensors.beverage_supply.unit',
                    location='sensors.beverage_supply.location',
                    name='sensors.beverage_supply.name',
                    description='sensors.beverage_supply.description',
                ),
            ),
            (
                'power_consumption',
                dict(
                    value=(
                        'sensors.power_consumption.value',
                        EnumConvert.INTEGER,
                    )
                ),
                dict(
                    unit='sensors.power_consumption.unit',
                    location='sensors.power_consumption.location',
                    name='sensors.power_consumption.name',
                    description='sensors.power_consumption.description',
                ),
            ),
            (
                'account_balance',
                dict(
                    value=(
                        'sensors.account_balance.value',
                        EnumConvert.NATURAL,
                    )
                ),
                dict(
                    unit='sensors.account_balance.unit',
                    location='sensors.account_balance.location',
                    name='sensors.account_balance.name',
                    description='sensors.account_balance.description',
                ),
            ),
            (
                'total_member_count',
                dict(
                    value=(
                        'sensors.total_member_count.value',
                        EnumConvert.INTEGER,
                    )
                ),
                dict(
                    location='sensors.total_member_count.location',
                    name='sensors.total_member_count.name',
                    description='sensors.total_member_count.description',
                ),
            ),
        ],
    )
    def test_sensors_common(field, sensors, fields, gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        result = []
        for idx in range(3):
            payload = {
                '_idx': idx,
                **{
                    key: Value.set(
                        key=f'{SP_API_PREFIX}.{field_key}',
                        idx=idx,
                        elem=field_key,
                    ).elem
                    for key, field_key in fields.items()
                },
            }

            for key, (sensor_key, convert) in sensors.items():
                sensor = gen_sensor(f'{sensor_key}-{idx}')
                sensor.append(user=user, value=idx)

                payload.update(
                    {
                        key: Value.set(
                            key=f'{SP_API_PREFIX}.{sensor_key}',
                            idx=idx,
                            elem=sensor,
                        ).latest.translate(
                            horizon=EnumHorizon.NORMAL,
                            convert=convert,
                            numeric=False,
                        )
                    }
                )

            result.append(payload)

        res = api.build()
        assert res['sensors'][field] == result

    @staticmethod
    @mark.parametrize('sub', ['alpha', 'beta', 'gamma', 'beta_gamma'])
    def test_sensors_radiation(sub, gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        result = []
        for idx in range(2):
            sensor = gen_sensor(f'value-{sub}-{idx}')
            sensor.append(user=user, value=idx)

            result.append(
                {
                    '_idx': idx,
                    'value': Value.set(
                        key=f'{SP_API_PREFIX}.sensors.radiation.{sub}.value',
                        idx=idx,
                        elem=sensor,
                    ).latest.translate(
                        horizon=EnumHorizon.NORMAL,
                        convert=EnumConvert.NATURAL,
                        numeric=False,
                    ),
                    **{
                        field: Value.set(
                            key=(
                                f'{SP_API_PREFIX}.sensors.'
                                f'radiation.{sub}.{field}'
                            ),
                            idx=idx,
                            elem=field,
                        ).elem
                        for field in [
                            'unit',
                            'dead_time',
                            'conversion_factor',
                            'location',
                            'name',
                            'description',
                        ]
                    },
                }
            )

        res = api.build()
        assert res['sensors']['radiation'][sub] == result

    @staticmethod
    def test_sensors_wind(gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        result = []
        for idx in range(2):
            payload = {'_idx': idx}

            properties = {}
            for prop, convert in [
                ('speed', EnumConvert.NATURAL),
                ('gust', EnumConvert.NATURAL),
                ('direction', EnumConvert.INTEGER),
                ('elevation', EnumConvert.INTEGER),
            ]:
                sensor = gen_sensor(f'{prop}-sensor-{idx}')
                sensor.append(user=user, value=idx)

                properties.update(
                    {
                        prop: {
                            'value': Value.set(
                                key=(
                                    f'{SP_API_PREFIX}.sensors.wind.'
                                    f'properties.{prop}.value'
                                ),
                                idx=idx,
                                elem=sensor,
                            ).latest.translate(
                                horizon=EnumHorizon.NORMAL,
                                convert=convert,
                                numeric=False,
                            ),
                            'unit': Value.set(
                                key=(
                                    f'{SP_API_PREFIX}.sensors.wind.'
                                    f'properties.{prop}.unit'
                                ),
                                idx=idx,
                                elem=f'{prop}-unit',
                            ).elem,
                        }
                    }
                )

            payload.update({'properties': properties})

            for key in ['location', 'name', 'description']:
                payload.update(
                    {
                        key: Value.set(
                            key=f'{SP_API_PREFIX}.sensors.wind.{key}',
                            idx=idx,
                            elem=key,
                        ).elem,
                    }
                )

            result.append(payload)

        res = api.build()
        assert res['sensors']['wind'] == result

    @staticmethod
    def test_sensors_network_traffic(gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        result = []
        for idx in range(2):
            bps_sensor = gen_sensor(f'bps-sensor-{idx}')
            bps_sensor.append(user=user, value=idx)
            pps_sensor = gen_sensor(f'pps-sensor-{idx}')
            pps_sensor.append(user=user, value=idx)

            payload = {
                '_idx': idx,
                'properties': {
                    'bits_per_second': {
                        'value': Value.set(
                            (
                                f'{SP_API_PREFIX}.sensors.network_traffic.'
                                'properties.bits_per_second.value'
                            ),
                            idx=idx,
                            elem=bps_sensor,
                        ).latest.value,
                        'maximum': Value.set(
                            (
                                f'{SP_API_PREFIX}.sensors.network_traffic.'
                                'properties.bits_per_second.maximum'
                            ),
                            idx=idx,
                            elem=idx * 5,
                        ).elem,
                    },
                    'packets_per_second': {
                        'value': Value.set(
                            (
                                f'{SP_API_PREFIX}.sensors.network_traffic.'
                                'properties.packets_per_second.value'
                            ),
                            idx=idx,
                            elem=pps_sensor,
                        ).latest.value,
                    },
                },
                **{
                    key: Value.set(
                        f'{SP_API_PREFIX}.sensors.network_traffic.{key}',
                        idx=idx,
                        elem=key,
                    ).elem
                    for key in ['location', 'name', 'description']
                },
            }
            result.append(payload)

        res = api.build()
        assert res['sensors']['network_traffic'] == result

    @staticmethod
    def test_projects():
        api = SpaceApi()
        one_pro = Value.set(
            key=f'{SP_API_PREFIX}.projects',
            idx=1,
            elem='https://example.org/mega',
        ).elem
        two_pro = Value.set(
            key=f'{SP_API_PREFIX}.projects',
            idx=2,
            elem='https://example.net/awesome',
        ).elem

        res = api.build()
        assert res['projects'] == [
            {'_idx': 1, 'value': one_pro},
            {'_idx': 2, 'value': two_pro},
        ]

    @staticmethod
    def test_links():
        api = SpaceApi()
        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.links.name', idx=0, elem='nil'
        ).elem
        Value.set(key=f'{SP_API_PREFIX}.links.name', idx=1, elem='one')
        two_name = Value.set(
            key=f'{SP_API_PREFIX}.links.name', idx=2, elem='two'
        ).elem

        nil_url = Value.set(
            key=f'{SP_API_PREFIX}.links.url',
            idx=0,
            elem='https://example.org',
        ).elem
        two_url = Value.set(
            key=f'{SP_API_PREFIX}.links.url',
            idx=2,
            elem='https://example.net',
        ).elem

        nil_desc = Value.set(
            key=f'{SP_API_PREFIX}.links.description', idx=0, elem='awesome'
        ).elem
        Value.set(key=f'{SP_API_PREFIX}.links.description', idx=1, elem='mega')

        res = api.build()
        assert res['links'] == [
            {
                '_idx': 0,
                'name': nil_name,
                'description': nil_desc,
                'url': nil_url,
            },
            {
                '_idx': 2,
                'name': two_name,
                'description': None,
                'url': two_url,
            },
        ]

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.name',
            idx=0,
            elem='standard',
        ).elem
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.name',
            idx=1,
            elem='premium',
        )
        two_name = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.name', idx=2, elem='deluxe'
        ).elem

        nil_value = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=0, elem=23.5
        ).elem
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=1, elem=42.0
        )
        two_value = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=2, elem=1337.0
        ).elem

        nil_curr = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=0,
            elem='EUR',
        ).elem
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=1,
            elem='GBP',
        )
        two_curr = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=2,
            elem='RUB',
        ).elem

        nil_int = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.billing_interval',
            idx=0,
            elem='daily',
        ).elem
        two_int = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.billing_interval',
            idx=2,
            elem='hourly',
        ).elem

        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.description',
            idx=1,
            elem='premium plan',
        )
        two_desc = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.description',
            idx=2,
            elem='deluxe plan',
        ).elem

        res = api.build()
        assert res['membership_plans'] == [
            {
                '_idx': 0,
                'name': nil_name,
                'value': nil_value,
                'currency': nil_curr,
                'billing_interval': nil_int,
                'description': None,
            },
            {
                '_idx': 2,
                'name': two_name,
                'value': two_value,
                'currency': two_curr,
                'billing_interval': two_int,
                'description': two_desc,
            },
        ]
