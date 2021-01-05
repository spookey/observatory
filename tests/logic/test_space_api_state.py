from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.values import Values
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiState:
    @staticmethod
    def test_empty():
        res = SpaceApi().get_state()
        assert res == {
            'icon': {'open': None, 'closed': None},
        }

    @staticmethod
    def test_icons():
        api = SpaceApi()

        opened = Values.set(
            key=f'{SP_API_PREFIX}.state.icon.open',
            idx=0,
            value='http://example.org/img/space-is-open.gif',
        ).value
        closed = Values.set(
            key=f'{SP_API_PREFIX}.state.icon.closed',
            idx=0,
            value='http://example.org/img/sorry-we-are-closed.gif',
        ).value

        res = api.get_state()
        assert res['icon']['open'] == opened
        assert res['icon']['closed'] == closed
