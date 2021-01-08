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
            Value.set(f'{SP_API_PREFIX}.cam', idx=idx, elem=f'cam #{idx}')

        assert api.cam_indices == indices

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        assert api.contact_keymasters_indices == []

        indices = list(range(5))
        for idx in indices:
            Value.set(
                choice(
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
    @mark.parametrize('field', ('temperature', 'barometer'))
    def test_sensors_value_unit_location(field):
        api = SpaceApi()
        assert getattr(api, f'sensors_{field}_indices', None) == []

        indices = list(range(choice(range(23, 42))))
        for idx in indices:
            Value.set(
                f'{SP_API_PREFIX}.sensors.{field}.value',
                idx=idx,
                elem=f'{field} #{idx} value',
            )
            Value.set(
                f'{SP_API_PREFIX}.sensors.{field}.unit',
                idx=idx,
                elem=f'{field} #{idx} unit',
            )
            Value.set(
                f'{SP_API_PREFIX}.sensors.{field}.location',
                idx=idx,
                elem=f'{field} #{idx} location',
            )

        assert getattr(api, f'sensors_{field}_indices', None) == indices

    @staticmethod
    def test_sensors_door_locked():
        api = SpaceApi()
        assert api.sensors_door_locked_indices == []

        indices = list(range(7))
        for idx in indices:
            Value.set(
                f'{SP_API_PREFIX}.sensors.door_locked.value',
                idx=idx,
                elem=f'door #{idx} locked value',
            )
            Value.set(
                f'{SP_API_PREFIX}.sensors.door_locked.location',
                idx=idx,
                elem=f'door #{idx} locked location',
            )

        assert api.sensors_door_locked_indices == indices

    @staticmethod
    def test_projects():
        api = SpaceApi()
        assert api.projects_indices == []

        indices = list(range(7))
        for idx in indices:
            Value.set(
                f'{SP_API_PREFIX}.projects', idx=idx, elem=f'project #{idx}'
            )

        assert api.projects_indices == indices

    @staticmethod
    def test_links():
        api = SpaceApi()
        assert api.links_indices == []

        indices = list(range(7))
        for idx in indices:
            Value.set(
                f'{SP_API_PREFIX}.links.name', idx=idx, elem=f'link #{idx}'
            )
            Value.set(
                f'{SP_API_PREFIX}.links.url', idx=idx, elem=f'url #{idx}'
            )

        assert api.links_indices == indices

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        assert api.membership_plans_indices == []

        indices = list(range(3))
        for idx in indices:
            Value.set(
                f'{SP_API_PREFIX}.membership_plans.name',
                idx=idx,
                elem=f'name #{idx}',
            )
            Value.set(
                f'{SP_API_PREFIX}.membership_plans.value', idx=idx, elem=idx
            )
            Value.set(
                f'{SP_API_PREFIX}.membership_plans.currency',
                idx=idx,
                elem=f'currency #{idx}',
            )
            Value.set(
                f'{SP_API_PREFIX}.membership_plans.billing_interval',
                idx=idx,
                elem=f'interval #{idx}',
            )

        assert api.membership_plans_indices == indices
