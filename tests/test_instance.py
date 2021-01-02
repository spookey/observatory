from observatory.instance import SPACE_API
from observatory.logic.space_api import SpaceApi


def test_space_api():
    assert SPACE_API is not None
    assert isinstance(SPACE_API, SpaceApi)
    assert getattr(SPACE_API, '_content', 'error') is None
    assert getattr(SPACE_API, '_last', 'error') is None
