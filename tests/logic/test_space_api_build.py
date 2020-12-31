from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.values import Values


@mark.usefixtures('session')
class TestSpaceApiBuild:
    @staticmethod
    def test_toplevel_fields():
        res = SpaceApi().build()
        assert sorted(res.keys()) == sorted(
            [
                'api_compatibility',
                'cam',
                'contact',
                'events',
                'feeds',
                'links',
                'location',
                'logo',
                'membership_plans',
                'projects',
                'sensors',
                'space',
                'spacefed',
                'state',
                'url',
            ]
        )

    @staticmethod
    def test_api_compatibility():
        res = SpaceApi().build()
        assert res['api_compatibility'] == ['14']

    @staticmethod
    def test_space_logo_url():
        api = SpaceApi()
        space = (
            Values.create(key='space_api.space', idx=0)
            .update(value='space')
            .value
        )
        logo = (
            Values.create(key='space_api.logo', idx=0)
            .update(value='https://example.org/image.gif')
            .value
        )
        url = (
            Values.create(key='space_api.url', idx=0)
            .update(value='https://example.net')
            .value
        )

        res = api.build()
        assert res['space'] == space
        assert res['logo'] == logo
        assert res['url'] == url

    @staticmethod
    def test_location_fields():
        res = SpaceApi().build()
        location = res['location']
        assert sorted(location.keys()) == sorted(
            [
                'address',
                'lat',
                'lon',
                'timezone',
            ]
        )

    @staticmethod
    def test_location():
        api = SpaceApi()
        address = (
            Values.create(key='space_api.location.address', idx=0)
            .update(value='Somewhere 23, 12345 FNORD')
            .value
        )
        lat = (
            Values.create(key='space_api.location.lat', idx=0)
            .update(value=23.5)
            .value
        )
        lon = (
            Values.create(key='space_api.location.lon', idx=0)
            .update(value=133.7)
            .value
        )
        timezone = (
            Values.create(key='space_api.location.timezone', idx=0)
            .update(value='UTC')
            .value
        )

        res = api.build()
        assert res['location']['address'] == address
        assert res['location']['lat'] == lat
        assert res['location']['lon'] == lon
        assert res['location']['timezone'] == timezone

    @staticmethod
    def test_spacefed_fields():
        res = SpaceApi().build()
        spacefed = res['spacefed']
        assert sorted(spacefed.keys()) == sorted(
            [
                'spacenet',
                'spacesaml',
            ]
        )

    @staticmethod
    def test_spacefed():
        api = SpaceApi()
        spacenet = (
            Values.create(key='space_api.spacefed.spacenet', idx=0)
            .update(value=True)
            .value
        )
        spacesaml = (
            Values.create(key='space_api.spacefed.spacesaml', idx=0)
            .update(value=False)
            .value
        )

        res = api.build()
        assert res['spacefed']['spacenet'] == spacenet
        assert res['spacefed']['spacesaml'] == spacesaml

    @staticmethod
    def test_cam():
        api = SpaceApi()
        nil_cam = (
            Values.create(key='space_api.cam', idx=0)
            .update(value='https://example.org/cam.mjpg')
            .value
        )
        two_cam = (
            Values.create(key='space_api.cam', idx=2)
            .update(value='https://example.com/webcam')
            .value
        )

        res = api.build()
        assert res['cam'] == [nil_cam, two_cam]

    @staticmethod
    def test_contact_fields():
        res = SpaceApi().build()
        contact = res['contact']
        assert sorted(contact.keys()) == sorted(
            [
                'email',
                'facebook',
                'foursquare',
                'gopher',
                'identica',
                'irc',
                'issue_mail',
                'keymasters',
                'mastodon',
                'matrix',
                'ml',
                'mumble',
                'phone',
                'sip',
                'twitter',
                'xmpp',
            ]
        )

    @staticmethod
    def test_contact_telephone():
        api = SpaceApi()
        phone = (
            Values.create(key='space_api.contact.phone', idx=0)
            .update(value='+1 234 567 890')
            .value
        )
        sip = (
            Values.create(key='space_api.contact.sip', idx=0)
            .update(value='sip:space@sip.example.org')
            .value
        )

        res = api.build()
        assert res['contact']['phone'] == phone
        assert res['contact']['sip'] == sip

    @staticmethod
    def test_contact_chats():
        api = SpaceApi()
        irc = (
            Values.create(key='space_api.contact.irc', idx=0)
            .update(value='irc://example.org/#space')
            .value
        )
        xmpp = (
            Values.create(key='space_api.contact.xmpp', idx=0)
            .update(value='chat@conference.example.org')
            .value
        )
        matrix = (
            Values.create(key='space_api.contact.matrix', idx=0)
            .update(value='#chat:example.org')
            .value
        )
        mumble = (
            Values.create(key='space_api.contact.mumble', idx=0)
            .update(value='mumble://mumble.example.org/space?version=0.0.1')
            .value
        )

        res = api.build()
        assert res['contact']['irc'] == irc
        assert res['contact']['xmpp'] == xmpp
        assert res['contact']['matrix'] == matrix
        assert res['contact']['mumble'] == mumble

    @staticmethod
    def test_contact_social():
        api = SpaceApi()
        twitter = (
            Values.create(key='space_api.contact.twitter', idx=0)
            .update(value='@space')
            .value
        )
        mastodon = (
            Values.create(key='space_api.contact.mastodon', idx=0)
            .update(value='@space@example.net')
            .value
        )
        facebook = (
            Values.create(key='space_api.contact.facebook', idx=0)
            .update(value='https://example.com/space')
            .value
        )
        identica = (
            Values.create(key='space_api.contact.identica', idx=0)
            .update(value='space@example.org')
            .value
        )

        res = api.build()
        assert res['contact']['twitter'] == twitter
        assert res['contact']['mastodon'] == mastodon
        assert res['contact']['facebook'] == facebook
        assert res['contact']['identica'] == identica

    @staticmethod
    def test_contact_network():
        api = SpaceApi()
        foursquare = (
            Values.create(key='space_api.contact.foursquare', idx=0)
            .update(value='000000000000000000000000')
            .value
        )
        gopher = (
            Values.create(key='space_api.contact.gopher', idx=0)
            .update(value='gopher://gopher.space.example.org')
            .value
        )

        res = api.build()
        assert res['contact']['foursquare'] == foursquare
        assert res['contact']['gopher'] == gopher

    @staticmethod
    def test_contact_mail():
        api = SpaceApi()
        email = (
            Values.create(key='space_api.contact.email', idx=0)
            .update(value='space@example.org')
            .value
        )
        mailinglist = (
            Values.create(key='space_api.contact.ml', idx=0)
            .update(value='list@example.org')
            .value
        )
        issue_mail = (
            Values.create(key='space_api.contact.issue_mail', idx=0)
            .update(value='space@example.org')
            .value
        )

        res = api.build()
        assert res['contact']['email'] == email
        assert res['contact']['ml'] == mailinglist
        assert res['contact']['issue_mail'] == issue_mail

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        nil_name = (
            Values.create(key='space_api.contact.keymasters.name', idx=0)
            .update(value='nil')
            .value
        )
        one_name = (
            Values.create(key='space_api.contact.keymasters.name', idx=1)
            .update(value='one')
            .value
        )
        Values.create(key='space_api.contact.keymasters.name', idx=2).update(
            value='two'
        )

        nil_phone = (
            Values.create(key='space_api.contact.keymasters.phone', idx=0)
            .update(value='+1 234 567 890')
            .value
        )
        nil_email = (
            Values.create(key='space_api.contact.keymasters.email', idx=0)
            .update(value='nil@example.org')
            .value
        )
        one_email = (
            Values.create(key='space_api.contact.keymasters.email', idx=1)
            .update(value='one@example.org')
            .value
        )
        one_xmpp = (
            Values.create(key='space_api.contact.keymasters.xmpp', idx=1)
            .update(value='one@jabber.example.org')
            .value
        )
        Values.create(key='space_api.contact.keymasters.xmpp', idx=2).update(
            value='two@jabber.example.org'
        )

        res = api.build()
        assert res['contact']['keymasters'] == [
            {
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
    def test_sensors_fields():
        res = SpaceApi().build()
        sensors = res['sensors']
        assert sorted(sensors.keys()) == sorted(
            [
                'account_balance',
                'barometer',
                'beverage_supply',
                'door_locked',
                'humidity',
                'network_connections',
                'network_traffic',
                'people_now_present',
                'power_consumption',
                'radiation',
                'temperature',
                'total_member_count',
                'wind',
            ]
        )

    @staticmethod
    def test_feeds_fields():
        res = SpaceApi().build()
        feeds = res['feeds']
        assert sorted(feeds.keys()) == sorted(
            [
                'blog',
                'calendar',
                'flickr',
                'wiki',
            ]
        )
        for elem in feeds.values():
            assert sorted(elem.keys()) == sorted(
                [
                    'type',
                    'url',
                ]
            )

    @staticmethod
    def test_projects():
        api = SpaceApi()
        one_pro = (
            Values.create(key='space_api.projects', idx=1)
            .update(value='https://example.org/mega')
            .value
        )
        two_pro = (
            Values.create(key='space_api.projects', idx=2)
            .update(value='https://example.net/awesome')
            .value
        )

        res = api.build()
        assert res['projects'] == [one_pro, two_pro]

    @staticmethod
    def test_links():
        api = SpaceApi()
        nil_name = (
            Values.create(key='space_api.links.name', idx=0)
            .update(value='nil')
            .value
        )
        Values.create(key='space_api.links.name', idx=1).update(value='one')
        two_name = (
            Values.create(key='space_api.links.name', idx=2)
            .update(value='two')
            .value
        )

        nil_url = (
            Values.create(key='space_api.links.url', idx=0)
            .update(value='https://example.org')
            .value
        )
        two_url = (
            Values.create(key='space_api.links.url', idx=2)
            .update(value='https://example.net')
            .value
        )

        nil_desc = (
            Values.create(key='space_api.links.description', idx=0)
            .update(value='awesome')
            .value
        )
        Values.create(key='space_api.links.description', idx=1).update(
            value='mega'
        )

        res = api.build()
        assert res['links'] == [
            {
                'name': nil_name,
                'description': nil_desc,
                'url': nil_url,
            },
            {
                'name': two_name,
                'description': None,
                'url': two_url,
            },
        ]

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        nil_name = (
            Values.create(key='space_api.membership_plans.name', idx=0)
            .update(value='standard')
            .value
        )
        Values.create(key='space_api.membership_plans.name', idx=1).update(
            value='premium'
        )
        two_name = (
            Values.create(key='space_api.membership_plans.name', idx=2)
            .update(value='deluxe')
            .value
        )

        nil_value = (
            Values.create(key='space_api.membership_plans.value', idx=0)
            .update(value=23.5)
            .value
        )
        Values.create(key='space_api.membership_plans.value', idx=1).update(
            value=42.0
        )
        two_value = (
            Values.create(key='space_api.membership_plans.value', idx=2)
            .update(value=1337.0)
            .value
        )

        nil_curr = (
            Values.create(key='space_api.membership_plans.currency', idx=0)
            .update(value='EUR')
            .value
        )
        Values.create(key='space_api.membership_plans.currency', idx=1).update(
            value='GBP'
        )
        two_curr = (
            Values.create(key='space_api.membership_plans.currency', idx=2)
            .update(value='RUB')
            .value
        )

        nil_int = (
            Values.create(
                key='space_api.membership_plans.billing_interval', idx=0
            )
            .update(value='daily')
            .value
        )
        two_int = (
            Values.create(
                key='space_api.membership_plans.billing_interval', idx=2
            )
            .update(value='hourly')
            .value
        )

        Values.create(
            key='space_api.membership_plans.description', idx=1
        ).update(value='premium plan')
        two_desc = (
            Values.create(key='space_api.membership_plans.description', idx=2)
            .update(value='deluxe plan')
            .value
        )

        res = api.build()
        assert res['membership_plans'] == [
            {
                'name': nil_name,
                'value': nil_value,
                'currency': nil_curr,
                'billing_interval': nil_int,
                'description': None,
            },
            {
                'name': two_name,
                'value': two_value,
                'currency': two_curr,
                'billing_interval': two_int,
                'description': two_desc,
            },
        ]
