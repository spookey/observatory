from pytest import mark

from observatory.logic.space_api import SpaceApi
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
            key=f'{SP_API_PREFIX}.space', idx=0, value='space'
        ).value
        logo = Value.set(
            key=f'{SP_API_PREFIX}.logo',
            idx=0,
            value='https://example.org/image.gif',
        ).value
        url = Value.set(
            key=f'{SP_API_PREFIX}.url', idx=0, value='https://example.net'
        ).value

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
            value='Somewhere 23, 12345 FNORD',
        ).value
        lat = Value.set(
            key=f'{SP_API_PREFIX}.location.lat', idx=0, value=23.5
        ).value
        lon = Value.set(
            key=f'{SP_API_PREFIX}.location.lon', idx=0, value=133.7
        ).value
        timezone = Value.set(
            key=f'{SP_API_PREFIX}.location.timezone', idx=0, value='UTC'
        ).value

        res = api.build()
        assert res['location']['address'] == address
        assert res['location']['lat'] == lat
        assert res['location']['lon'] == lon
        assert res['location']['timezone'] == timezone

    @staticmethod
    def test_spacefed():
        api = SpaceApi()
        spacenet = Value.set(
            key=f'{SP_API_PREFIX}.spacefed.spacenet', idx=0, value=True
        ).value
        spacesaml = Value.set(
            key=f'{SP_API_PREFIX}.spacefed.spacesaml', idx=0, value=False
        ).value

        res = api.build()
        assert res['spacefed']['spacenet'] == spacenet
        assert res['spacefed']['spacesaml'] == spacesaml

    @staticmethod
    def test_cam():
        api = SpaceApi()
        nil_cam = Value.set(
            key=f'{SP_API_PREFIX}.cam',
            idx=0,
            value='https://example.org/cam.mjpg',
        ).value
        two_cam = Value.set(
            key=f'{SP_API_PREFIX}.cam',
            idx=2,
            value='https://example.com/webcam',
        ).value

        res = api.build()
        assert res['cam'] == [
            {'_idx': 0, 'value': nil_cam},
            {'_idx': 2, 'value': two_cam},
        ]

    @staticmethod
    def test_contact_telephone():
        api = SpaceApi()
        phone = Value.set(
            key=f'{SP_API_PREFIX}.contact.phone', idx=0, value='+1 234 567 890'
        ).value
        sip = Value.set(
            key=f'{SP_API_PREFIX}.contact.sip',
            idx=0,
            value='sip:space@sip.example.org',
        ).value

        res = api.build()
        assert res['contact']['phone'] == phone
        assert res['contact']['sip'] == sip

    @staticmethod
    def test_contact_chats():
        api = SpaceApi()
        irc = Value.set(
            key=f'{SP_API_PREFIX}.contact.irc',
            idx=0,
            value='irc://example.org/#space',
        ).value
        xmpp = Value.set(
            key=f'{SP_API_PREFIX}.contact.xmpp',
            idx=0,
            value='chat@conference.example.org',
        ).value
        matrix = Value.set(
            key=f'{SP_API_PREFIX}.contact.matrix',
            idx=0,
            value='#chat:example.org',
        ).value
        mumble = Value.set(
            key=f'{SP_API_PREFIX}.contact.mumble',
            idx=0,
            value='mumble://mumble.example.org/space?version=0.0.1',
        ).value

        res = api.build()
        assert res['contact']['irc'] == irc
        assert res['contact']['xmpp'] == xmpp
        assert res['contact']['matrix'] == matrix
        assert res['contact']['mumble'] == mumble

    @staticmethod
    def test_contact_social():
        api = SpaceApi()
        twitter = Value.set(
            key=f'{SP_API_PREFIX}.contact.twitter', idx=0, value='@space'
        ).value
        mastodon = Value.set(
            key=f'{SP_API_PREFIX}.contact.mastodon',
            idx=0,
            value='@space@example.net',
        ).value
        facebook = Value.set(
            key=f'{SP_API_PREFIX}.contact.facebook',
            idx=0,
            value='https://example.com/space',
        ).value
        identica = Value.set(
            key=f'{SP_API_PREFIX}.contact.identica',
            idx=0,
            value='space@example.org',
        ).value

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
            value='000000000000000000000000',
        ).value
        gopher = Value.set(
            key=f'{SP_API_PREFIX}.contact.gopher',
            idx=0,
            value='gopher://gopher.space.example.org',
        ).value

        res = api.build()
        assert res['contact']['foursquare'] == foursquare
        assert res['contact']['gopher'] == gopher

    @staticmethod
    def test_contact_mail():
        api = SpaceApi()
        email = Value.set(
            key=f'{SP_API_PREFIX}.contact.email',
            idx=0,
            value='space@example.org',
        ).value
        mailinglist = Value.set(
            key=f'{SP_API_PREFIX}.contact.ml', idx=0, value='list@example.org'
        ).value
        issue_mail = Value.set(
            key=f'{SP_API_PREFIX}.contact.issue_mail',
            idx=0,
            value='space@example.org',
        ).value

        res = api.build()
        assert res['contact']['email'] == email
        assert res['contact']['ml'] == mailinglist
        assert res['contact']['issue_mail'] == issue_mail

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=0, value='nil'
        ).value
        one_name = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=1, value='one'
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.name', idx=2, value='two'
        )

        nil_phone = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.phone',
            idx=0,
            value='+1 234 567 890',
        ).value
        nil_email = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.email',
            idx=0,
            value='nil@example.org',
        ).value
        one_email = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.email',
            idx=1,
            value='one@example.org',
        ).value
        one_xmpp = Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.xmpp',
            idx=1,
            value='one@jabber.example.org',
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.contact.keymasters.xmpp',
            idx=2,
            value='two@jabber.example.org',
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
    def test_projects():
        api = SpaceApi()
        one_pro = Value.set(
            key=f'{SP_API_PREFIX}.projects',
            idx=1,
            value='https://example.org/mega',
        ).value
        two_pro = Value.set(
            key=f'{SP_API_PREFIX}.projects',
            idx=2,
            value='https://example.net/awesome',
        ).value

        res = api.build()
        assert res['projects'] == [
            {'_idx': 1, 'value': one_pro},
            {'_idx': 2, 'value': two_pro},
        ]

    @staticmethod
    def test_links():
        api = SpaceApi()
        nil_name = Value.set(
            key=f'{SP_API_PREFIX}.links.name', idx=0, value='nil'
        ).value
        Value.set(key=f'{SP_API_PREFIX}.links.name', idx=1, value='one')
        two_name = Value.set(
            key=f'{SP_API_PREFIX}.links.name', idx=2, value='two'
        ).value

        nil_url = Value.set(
            key=f'{SP_API_PREFIX}.links.url',
            idx=0,
            value='https://example.org',
        ).value
        two_url = Value.set(
            key=f'{SP_API_PREFIX}.links.url',
            idx=2,
            value='https://example.net',
        ).value

        nil_desc = Value.set(
            key=f'{SP_API_PREFIX}.links.description', idx=0, value='awesome'
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.links.description', idx=1, value='mega'
        )

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
            value='standard',
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.name',
            idx=1,
            value='premium',
        )
        two_name = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.name', idx=2, value='deluxe'
        ).value

        nil_value = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=0, value=23.5
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=1, value=42.0
        )
        two_value = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.value', idx=2, value=1337.0
        ).value

        nil_curr = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=0,
            value='EUR',
        ).value
        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=1,
            value='GBP',
        )
        two_curr = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.currency',
            idx=2,
            value='RUB',
        ).value

        nil_int = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.billing_interval',
            idx=0,
            value='daily',
        ).value
        two_int = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.billing_interval',
            idx=2,
            value='hourly',
        ).value

        Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.description',
            idx=1,
            value='premium plan',
        )
        two_desc = Value.set(
            key=f'{SP_API_PREFIX}.membership_plans.description',
            idx=2,
            value='deluxe plan',
        ).value

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
