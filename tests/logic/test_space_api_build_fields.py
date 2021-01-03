from pytest import mark

from observatory.logic.space_api import SpaceApi


@mark.usefixtures('session')
class TestSpaceApiBuildFields:
    @staticmethod
    def test_toplevel():
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
    def test_location():
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
    def test_spacefed():
        res = SpaceApi().build()
        spacefed = res['spacefed']
        assert sorted(spacefed.keys()) == sorted(
            [
                'spacenet',
                'spacesaml',
            ]
        )

    @staticmethod
    def test_contact():
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
    def test_sensors():
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
    def test_sensors_radiation():
        res = SpaceApi().build()
        radiation = res['sensors']['radiation']
        assert sorted(radiation.keys()) == sorted(
            [
                'alpha',
                'beta',
                'beta_gamma',
                'gamma',
            ]
        )

    @staticmethod
    def test_feeds():
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
