from pytest import mark

from observatory.logic.space_api import SpaceApi


@mark.usefixtures('session')
class TestSpaceApiState:
    @staticmethod
    def test_state():
        api = SpaceApi()

        assert api.get_state() == {}

    @staticmethod
    def test_todo():
        todo = True
        assert todo
