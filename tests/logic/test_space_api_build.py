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
        space, logo, url = (
            'space',
            'https://example.org/image.gif',
            'https://example.net',
        )
        Values.create(key='space', idx=0).update(value=space)
        Values.create(key='logo', idx=0).update(value=logo)
        Values.create(key='url', idx=0).update(value=url)

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
        address, lat, lon, timezone = (
            'Somewhere 23, 12345 FNORD',
            23.5,
            133.7,
            'UTC',
        )
        Values.create(key='location.address', idx=0).update(value=address)
        Values.create(key='location.lat', idx=0).update(value=lat)
        Values.create(key='location.lon', idx=0).update(value=lon)
        Values.create(key='location.timezone', idx=0).update(value=timezone)

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
        spacenet, spacesaml = True, False
        Values.create(key='spacefed.spacenet', idx=0).update(value=spacenet)
        Values.create(key='spacefed.spacesaml', idx=0).update(value=spacesaml)

        res = api.build()
        assert res['spacefed']['spacenet'] == spacenet
        assert res['spacefed']['spacesaml'] == spacesaml

    @staticmethod
    def test_cam():
        api = SpaceApi()
        nil_cam, two_cam = (
            'https://example.org/cam.mjpg',
            'https://example.com/webcam',
        )
        Values.create(key='cam', idx=0).update(value=nil_cam)
        Values.create(key='cam', idx=2).update(value=two_cam)

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
        phone, sip = '+1 234 567 890', 'sip:space@sip.example.org'
        Values.create(key='contact.phone', idx=0).update(value=phone)
        Values.create(key='contact.sip', idx=0).update(value=sip)

        res = api.build()
        assert res['contact']['phone'] == phone
        assert res['contact']['sip'] == sip

    @staticmethod
    def test_contact_chats():
        api = SpaceApi()
        irc, xmpp, matrix, mumble = (
            'irc://example.org/#space',
            'chat@conference.example.org',
            '#chat:example.org',
            'mumble://mumble.example.org/space?version=0.0.1',
        )

        Values.create(key='contact.irc', idx=0).update(value=irc)
        Values.create(key='contact.xmpp', idx=0).update(value=xmpp)
        Values.create(key='contact.matrix', idx=0).update(value=matrix)
        Values.create(key='contact.mumble', idx=0).update(value=mumble)

        res = api.build()
        assert res['contact']['irc'] == irc
        assert res['contact']['xmpp'] == xmpp
        assert res['contact']['matrix'] == matrix
        assert res['contact']['mumble'] == mumble

    @staticmethod
    def test_contact_social():
        api = SpaceApi()
        twitter, mastodon, facebook, identica = (
            '@space',
            '@space@example.net',
            'https://example.com/space',
            'space@example.org',
        )
        Values.create(key='contact.twitter', idx=0).update(value=twitter)
        Values.create(key='contact.mastodon', idx=0).update(value=mastodon)
        Values.create(key='contact.facebook', idx=0).update(value=facebook)
        Values.create(key='contact.identica', idx=0).update(value=identica)

        res = api.build()
        assert res['contact']['twitter'] == twitter
        assert res['contact']['mastodon'] == mastodon
        assert res['contact']['facebook'] == facebook
        assert res['contact']['identica'] == identica

    @staticmethod
    def test_contact_network():
        api = SpaceApi()
        foursquare, gopher = (
            '000000000000000000000000',
            'gopher://gopher.space.example.org',
        )
        Values.create(key='contact.foursquare', idx=0).update(value=foursquare)
        Values.create(key='contact.gopher', idx=0).update(value=gopher)

        res = api.build()
        assert res['contact']['foursquare'] == foursquare
        assert res['contact']['gopher'] == gopher

    @staticmethod
    def test_contact_mail():
        api = SpaceApi()
        email, mailinglist, issue_mail = (
            'space@example.org',
            'list@example.org',
            'space@example.org',
        )
        Values.create(key='contact.email', idx=0).update(value=email)
        Values.create(key='contact.ml', idx=0).update(value=mailinglist)
        Values.create(key='contact.issue_mail', idx=0).update(value=issue_mail)

        res = api.build()

        assert res['contact']['email'] == email
        assert res['contact']['ml'] == mailinglist
        assert res['contact']['issue_mail'] == issue_mail

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        nil_name, one_name, two_name = 'nil', 'one', 'two'
        Values.create(key='contact.keymasters.name', idx=0).update(
            value=nil_name
        )
        Values.create(key='contact.keymasters.name', idx=1).update(
            value=one_name
        )
        Values.create(key='contact.keymasters.name', idx=2).update(
            value=two_name
        )

        nil_phone, nil_email = ('+1 234 567 890', 'nil@example.org')
        one_email, one_xmpp = ('one@example.org', 'one@jabber.example.org')
        two_xmpp = 'two@jabber.example.org'
        Values.create(key='contact.keymasters.phone', idx=0).update(
            value=nil_phone
        )
        Values.create(key='contact.keymasters.email', idx=0).update(
            value=nil_email
        )
        Values.create(key='contact.keymasters.email', idx=1).update(
            value=one_email
        )
        Values.create(key='contact.keymasters.xmpp', idx=1).update(
            value=one_xmpp
        )
        Values.create(key='contact.keymasters.xmpp', idx=2).update(
            value=two_xmpp
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
        one_pro, two_pro = (
            'https://example.org/mega',
            'https://example.net/awesome',
        )
        Values.create(key='projects', idx=1).update(value=one_pro)
        Values.create(key='projects', idx=2).update(value=two_pro)

        res = api.build()
        assert res['projects'] == [one_pro, two_pro]

    @staticmethod
    def test_links():
        api = SpaceApi()

        nil_name, one_name, two_name = 'nil', 'one', 'two'
        Values.create(key='links.name', idx=0).update(value=nil_name)
        Values.create(key='links.name', idx=1).update(value=one_name)
        Values.create(key='links.name', idx=2).update(value=two_name)

        nil_url, two_url = (
            'https://example.org',
            'https://example.net',
        )
        Values.create(key='links.url', idx=0).update(value=nil_url)
        Values.create(key='links.url', idx=2).update(value=two_url)

        nil_desc, one_desc = ('awesome', 'mega')
        Values.create(key='links.description', idx=0).update(value=nil_desc)
        Values.create(key='links.description', idx=1).update(value=one_desc)

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

        nil_name, one_name, two_name = 'standard', 'premium', 'deluxe'
        Values.create(key='membership_plans.name', idx=0).update(
            value=nil_name
        )
        Values.create(key='membership_plans.name', idx=1).update(
            value=one_name
        )
        Values.create(key='membership_plans.name', idx=2).update(
            value=two_name
        )

        nil_value, one_value, two_value = 23.0, 42.0, 1337.0
        Values.create(key='membership_plans.value', idx=0).update(
            value=nil_value
        )
        Values.create(key='membership_plans.value', idx=1).update(
            value=one_value
        )
        Values.create(key='membership_plans.value', idx=2).update(
            value=two_value
        )

        nil_curr, one_curr, two_curr = 'EUR', 'GBP', 'RUB'
        Values.create(key='membership_plans.currency', idx=0).update(
            value=nil_curr
        )
        Values.create(key='membership_plans.currency', idx=1).update(
            value=one_curr
        )
        Values.create(key='membership_plans.currency', idx=2).update(
            value=two_curr
        )

        nil_int, two_int = 'daily', 'hourly'
        Values.create(key='membership_plans.billing_interval', idx=0).update(
            value=nil_int
        )
        Values.create(key='membership_plans.billing_interval', idx=2).update(
            value=two_int
        )

        one_desc, two_desc = 'premium plan', 'deluxe plan'
        Values.create(key='membership_plans.description', idx=1).update(
            value=one_desc
        )
        Values.create(key='membership_plans.description', idx=2).update(
            value=two_desc
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
