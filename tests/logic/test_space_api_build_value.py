from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX

# pylint: disable=too-many-locals


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
    def test_sensors_temperature(gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()
        nil_sensor = gen_sensor('nil')
        nil_sensor.append(user=user, value=0)
        nil_value = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.value',
            idx=0,
            elem=nil_sensor,
        ).latest.value
        one_sensor = gen_sensor('one')
        one_sensor.append(user=user, value=1)
        one_value = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.value',
            idx=1,
            elem=one_sensor,
        ).latest.value

        nil_unit = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.unit',
            idx=0,
            elem='hot',
        ).elem
        one_unit = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.unit',
            idx=1,
            elem='cold',
        ).elem

        nil_location = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.location',
            idx=0,
            elem='below',
        ).elem
        one_location = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.location',
            idx=1,
            elem='above',
        ).elem

        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.name',
            idx=0,
            elem='sensor #0',
        ).elem
        one_name = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.name',
            idx=1,
            elem='sensor #1',
        ).elem

        nil_description = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.description',
            idx=0,
            elem='temperature sensor #0',
        ).elem
        one_description = Value.set(
            key=f'{SP_API_PREFIX}.sensors.temperature.description',
            idx=1,
            elem='temperature sensor #1',
        ).elem

        res = api.build()
        assert res['sensors']['temperature'] == [
            {
                '_idx': 0,
                'value': nil_value,
                'unit': nil_unit,
                'location': nil_location,
                'name': nil_name,
                'description': nil_description,
            },
            {
                '_idx': 1,
                'value': one_value,
                'unit': one_unit,
                'location': one_location,
                'name': one_name,
                'description': one_description,
            },
        ]

    @staticmethod
    def test_sensors_door_locked(gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        nil_sensor = gen_sensor('nil')
        nil_sensor.append(user=user, value=1)
        nil_value = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.value',
            idx=0,
            elem=nil_sensor,
        ).latest.value
        one_sensor = gen_sensor('one')
        one_sensor.append(user=user, value=0)
        one_value = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.value',
            idx=1,
            elem=one_sensor,
        ).latest.value

        nil_location = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.location',
            idx=0,
            elem='main',
        ).elem
        one_location = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.location',
            idx=1,
            elem='side',
        ).elem

        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.name',
            idx=0,
            elem='sensor #0',
        ).elem
        one_name = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.name',
            idx=1,
            elem='sensor #1',
        ).elem

        nil_description = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.description',
            idx=0,
            elem='door lock sensor #0',
        ).elem
        one_description = Value.set(
            key=f'{SP_API_PREFIX}.sensors.door_locked.description',
            idx=1,
            elem='door lock sensor #1',
        ).elem

        res = api.build()
        assert res['sensors']['door_locked'] == [
            {
                '_idx': 0,
                'value': nil_value,
                'location': nil_location,
                'name': nil_name,
                'description': nil_description,
            },
            {
                '_idx': 1,
                'value': one_value,
                'location': one_location,
                'name': one_name,
                'description': one_description,
            },
        ]

    @staticmethod
    def test_sensors_barometer(gen_sensor, gen_user):
        api = SpaceApi()
        user = gen_user()

        one_sensor = gen_sensor('one')
        one_sensor.append(user=user, value=1)
        one_value = Value.set(
            key=f'{SP_API_PREFIX}.sensors.barometer.value',
            idx=1,
            elem=one_sensor,
        ).latest.value

        one_unit = Value.set(
            key=f'{SP_API_PREFIX}.sensors.barometer.unit',
            idx=1,
            elem='high',
        ).elem

        one_location = Value.set(
            key=f'{SP_API_PREFIX}.sensors.barometer.location',
            idx=1,
            elem='somewhere',
        ).elem

        one_name = Value.set(
            key=f'{SP_API_PREFIX}.sensors.barometer.name',
            idx=1,
            elem='sensor #1',
        ).elem

        one_description = Value.set(
            key=f'{SP_API_PREFIX}.sensors.barometer.description',
            idx=1,
            elem='barometer #1',
        ).elem

        res = api.build()
        assert res['sensors']['barometer'] == [
            {
                '_idx': 1,
                'value': one_value,
                'unit': one_unit,
                'location': one_location,
                'name': one_name,
                'description': one_description,
            },
        ]

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
