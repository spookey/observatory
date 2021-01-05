from datetime import datetime, timedelta

from pytest import fixture

from observatory.logic.space_api import SpaceApi
from observatory.start.environment import SP_API_REFRESH

VERY_OLD = datetime.utcnow() - timedelta(seconds=23 * SP_API_REFRESH)
CONTENT = {
    'very': 'important',
    'test': 'content',
}
STATE = {'broken': True}
EVENTS = ['hardcore', 'party', 'action']

# pylint: disable=redefined-outer-name


@fixture(scope='function')
def api(monkeypatch):
    obj = SpaceApi()

    def res():
        pass

    def _inner_content(value):
        monkeypatch.setattr(obj, '_content', value)

    def _inner_last(value):
        monkeypatch.setattr(obj, '_last', value)

    def build_fn(value):
        monkeypatch.setattr(obj, 'build', lambda: value)

    res.obj = obj
    res.inner_content = _inner_content
    res.inner_last = _inner_last
    res.build_fn = build_fn

    yield res


class TestSpaceApiClass:
    @staticmethod
    def test_initial(api):
        assert getattr(api.obj, '_content', 'error') is None
        assert getattr(api.obj, '_last', 'error') is None

    @staticmethod
    def test_outdated(api):
        api.inner_content(None)
        api.inner_last(None)
        assert api.obj.outdated is True

        api.inner_content({})
        api.inner_last(None)
        assert api.obj.outdated is True

        api.inner_content({})
        api.inner_last(VERY_OLD)
        assert api.obj.outdated is True

        api.inner_content({})
        api.inner_last(datetime.utcnow())
        assert api.obj.outdated is False

    @staticmethod
    def test_content_property(api):
        past = datetime.utcnow()

        assert getattr(api.obj, '_content', 'error') is None
        assert getattr(api.obj, '_last', 'error') is None

        api.build_fn(CONTENT)

        assert api.obj.content == CONTENT

        assert getattr(api.obj, '_content', 'error') == CONTENT
        last = getattr(api.obj, '_last', 'error')
        assert last >= past
        assert last < datetime.utcnow()

    @staticmethod
    def test_clear_method(api):
        assert getattr(api.obj, '_content', 'error') is None
        assert getattr(api.obj, '_last', 'error') is None

        api.inner_content(CONTENT)
        api.inner_last(VERY_OLD)

        assert getattr(api.obj, '_content', 'error') == CONTENT
        assert getattr(api.obj, '_last', 'error') == VERY_OLD

        assert api.obj.clear()

        assert getattr(api.obj, '_content', 'error') is None
        assert getattr(api.obj, '_last', 'error') is None

    @staticmethod
    def test_reset_method(api):
        past = datetime.utcnow()

        assert getattr(api.obj, '_content', 'error') is None
        assert getattr(api.obj, '_last', 'error') is None

        new_content = dict(state=STATE, events=EVENTS, **CONTENT)
        api.build_fn(new_content)
        api.inner_content(CONTENT)
        api.inner_last(past)

        assert getattr(api.obj, '_content', 'error') == CONTENT
        assert getattr(api.obj, '_last', 'error') == past

        assert api.obj.content == CONTENT

        assert api.obj.reset()

        assert getattr(api.obj, '_content', 'error') == new_content
        last = getattr(api.obj, '_last', 'error')
        assert last >= past
        assert last < datetime.utcnow()
