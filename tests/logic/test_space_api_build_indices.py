from random import choice

from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.values import Values
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
            Values.set(f'{SP_API_PREFIX}.cam', idx=idx, value=f'cam #{idx}')

        assert api.cam_indices == indices

    @staticmethod
    def test_contact_keymasters():
        api = SpaceApi()
        assert api.concact_keymasters_indices == []

        indices = list(range(5))
        for idx in indices:
            Values.set(
                choice(
                    [
                        f'{SP_API_PREFIX}.contact.keymasters.irc_nick',
                        f'{SP_API_PREFIX}.contact.keymasters.phone',
                        f'{SP_API_PREFIX}.contact.keymasters.email',
                        f'{SP_API_PREFIX}.contact.keymasters.twitter',
                    ]
                ),
                idx=idx,
                value=f'keymaster #{idx}',
            )

        assert api.concact_keymasters_indices == indices

    @staticmethod
    def test_projects():
        api = SpaceApi()
        assert api.projects_indices == []

        indices = list(range(7))
        for idx in indices:
            Values.set(
                f'{SP_API_PREFIX}.projects', idx=idx, value=f'project #{idx}'
            )

        assert api.projects_indices == indices

    @staticmethod
    def test_links():
        api = SpaceApi()
        assert api.links_indices == []

        indices = list(range(7))
        for idx in indices:
            Values.set(
                f'{SP_API_PREFIX}.links.name', idx=idx, value=f'link #{idx}'
            )
            Values.set(
                f'{SP_API_PREFIX}.links.url', idx=idx, value=f'url #{idx}'
            )

        assert api.links_indices == indices

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        assert api.membership_plans_indices == []

        indices = list(range(3))
        for idx in indices:
            Values.set(
                f'{SP_API_PREFIX}.membership_plans.name',
                idx=idx,
                value=f'name #{idx}',
            )
            Values.set(
                f'{SP_API_PREFIX}.membership_plans.value', idx=idx, value=idx
            )
            Values.set(
                f'{SP_API_PREFIX}.membership_plans.currency',
                idx=idx,
                value=f'currency #{idx}',
            )
            Values.set(
                f'{SP_API_PREFIX}.membership_plans.billing_interval',
                idx=idx,
                value=f'interval #{idx}',
            )

        assert api.membership_plans_indices == indices
