from random import choice

from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.values import Values


@mark.usefixtures('session')
class TestSpaceApiBuildIndices:
    @staticmethod
    def test_cam():
        api = SpaceApi()
        assert api.cam_indices == []

        indices = list(range(5))
        for idx in indices:
            Values.set('space_api.cam', idx=idx, value=f'cam #{idx}')

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
                        'space_api.contact.keymasters.irc_nick',
                        'space_api.contact.keymasters.phone',
                        'space_api.contact.keymasters.email',
                        'space_api.contact.keymasters.twitter',
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
            Values.set('space_api.projects', idx=idx, value=f'project #{idx}')

        assert api.projects_indices == indices

    @staticmethod
    def test_links():
        api = SpaceApi()
        assert api.links_indices == []

        indices = list(range(7))
        for idx in indices:
            Values.set('space_api.links.name', idx=idx, value=f'link #{idx}')
            Values.set('space_api.links.url', idx=idx, value=f'url #{idx}')

        assert api.links_indices == indices

    @staticmethod
    def test_membership_plans():
        api = SpaceApi()
        assert api.membership_plans_indices == []

        indices = list(range(3))
        for idx in indices:
            Values.set(
                'space_api.membership_plans.name',
                idx=idx,
                value=f'name #{idx}',
            )
            Values.set('space_api.membership_plans.value', idx=idx, value=idx)
            Values.set(
                'space_api.membership_plans.currency',
                idx=idx,
                value=f'currency #{idx}',
            )
            Values.set(
                'space_api.membership_plans.billing_interval',
                idx=idx,
                value=f'interval #{idx}',
            )

        assert api.membership_plans_indices == indices
