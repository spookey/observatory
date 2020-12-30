from pytest import mark

from observatory.logic.space_api import SpaceApi


@mark.usefixtures('session')
class TestSpaceApiState:
    @staticmethod
    def test_events():
        api = SpaceApi()

        assert api.get_events() == []

    @staticmethod
    def test_todo():
        todo = True
        assert todo
