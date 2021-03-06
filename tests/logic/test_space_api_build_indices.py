from random import choice

from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiBuildIndices:
    @staticmethod
    def test_next_index():
        func = SpaceApi.next_index
        assert func(None) == 0
        assert func(list()) == 0
        assert func(set()) == 0
        assert func([1, 2, 3]) == 0
        assert func([0, 2, 3]) == 1
        assert func([0, 1, 3]) == 2
        assert func([0, 1, 2]) == 3

    @staticmethod
    def test_cam():
        api = SpaceApi()
        assert api.cam_indices == []

        indices = list(range(5))
        for idx in indices:
            Value.set(key=f'{SP_API_PREFIX}.cam', idx=idx, elem=f'cam #{idx}')

        assert api.cam_indices == indices

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        assert api.contact_keymasters_indices == []

        indices = list(range(5))
        for idx in indices:
            Value.set(
                key=choice(
                    [
                        f'{SP_API_PREFIX}.contact.keymasters.irc_nick',
                        f'{SP_API_PREFIX}.contact.keymasters.phone',
                        f'{SP_API_PREFIX}.contact.keymasters.email',
                        f'{SP_API_PREFIX}.contact.keymasters.twitter',
                    ]
                ),
                idx=idx,
                elem=f'keymaster #{idx}',
            )

        assert api.contact_keymasters_indices == indices

    @staticmethod
    @mark.parametrize(
        ('field', 'keys'),
        [
            (
                'temperature',
                [
                    'sensors.temperature.value',
                    'sensors.temperature.unit',
                    'sensors.temperature.location',
                ],
            ),
            (
                'door_locked',
                ['sensors.door_locked.value', 'sensors.door_locked.location'],
            ),
            (
                'barometer',
                [
                    'sensors.barometer.value',
                    'sensors.barometer.unit',
                    'sensors.barometer.location',
                ],
            ),
            (
                'humidity',
                [
                    'sensors.humidity.value',
                    'sensors.humidity.unit',
                    'sensors.humidity.location',
                ],
            ),
            (
                'beverage_supply',
                [
                    'sensors.beverage_supply.value',
                    'sensors.beverage_supply.unit',
                ],
            ),
            (
                'power_consumption',
                [
                    'sensors.power_consumption.value',
                    'sensors.power_consumption.unit',
                    'sensors.power_consumption.location',
                ],
            ),
            (
                'wind',
                [
                    'sensors.wind.properties.speed.value',
                    'sensors.wind.properties.speed.unit',
                    'sensors.wind.properties.gust.value',
                    'sensors.wind.properties.gust.unit',
                    'sensors.wind.properties.direction.value',
                    'sensors.wind.properties.direction.unit',
                    'sensors.wind.properties.elevation.value',
                    'sensors.wind.properties.elevation.unit',
                    'sensors.wind.location',
                ],
            ),
            (
                'account_balance',
                [
                    'sensors.account_balance.value',
                    'sensors.account_balance.unit',
                ],
            ),
            ('total_member_count', ['sensors.total_member_count.value']),
            (
                'network_traffic',
                [
                    'sensors.network_traffic.properties.bits_per_second.value',
                    (
                        'sensors.network_traffic.properties'
                        '.packets_per_second.value'
                    ),
                ],
            ),
        ],
    )
    def test_sensors_common(field, keys):
        api = SpaceApi()
        assert getattr(api, f'sensors_{field}_indices', None) == []

        indices = list(range(4))
        for idx in indices:
            for key in keys:
                Value.set(
                    key=f'{SP_API_PREFIX}.{key}',
                    idx=idx,
                    elem=f'{field} #{idx} {key}',
                )

        assert getattr(api, f'sensors_{field}_indices', None) == indices

    @staticmethod
    @mark.parametrize('sub', ['alpha', 'beta', 'gamma', 'beta_gamma'])
    def test_sensors_radiation(sub):
        api = SpaceApi()
        assert api.sensors_radiation_indices(sub) == []

        indices = list(range(5))
        for idx in indices:
            for key in ['value', 'unit']:
                Value.set(
                    key=f'{SP_API_PREFIX}.sensors.radiation.{sub}.{key}',
                    idx=idx,
                    elem=f'radiation {sub} #{idx} {key}',
                )

        assert api.sensors_radiation_indices(sub) == indices

    @staticmethod
    def test_projects():
        api = SpaceApi()
        assert api.projects_indices == []

        indices = list(range(7))
        for idx in indices:
            Value.set(
                key=f'{SP_API_PREFIX}.projects',
                idx=idx,
                elem=f'project #{idx}',
            )

        assert api.projects_indices == indices

    @staticmethod
    def test_links():
        api = SpaceApi()
        assert api.links_indices == []

        indices = list(range(7))
        for idx in indices:
            Value.set(
                key=f'{SP_API_PREFIX}.links.name', idx=idx, elem=f'link #{idx}'
            )
            Value.set(
                key=f'{SP_API_PREFIX}.links.url', idx=idx, elem=f'url #{idx}'
            )

        assert api.links_indices == indices

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        assert api.membership_plans_indices == []

        indices = list(range(3))
        for idx in indices:
            Value.set(
                key=f'{SP_API_PREFIX}.membership_plans.name',
                idx=idx,
                elem=f'name #{idx}',
            )
            Value.set(
                key=f'{SP_API_PREFIX}.membership_plans.value',
                idx=idx,
                elem=idx,
            )
            Value.set(
                key=f'{SP_API_PREFIX}.membership_plans.currency',
                idx=idx,
                elem=f'currency #{idx}',
            )
            Value.set(
                key=f'{SP_API_PREFIX}.membership_plans.billing_interval',
                idx=idx,
                elem=f'interval #{idx}',
            )

        assert api.membership_plans_indices == indices
