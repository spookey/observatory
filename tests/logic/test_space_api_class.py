from datetime import datetime, timedelta

from observatory.logic.space_api import SpaceApi
from observatory.start.environment import SP_API_REFRESH


class TestSpaceApiClass:
    @staticmethod
    def test_initial():
        obj = SpaceApi()
        assert getattr(obj, '_content', 'error') is None
        assert getattr(obj, '_last', 'error') is None

    @staticmethod
    def test_outdated(monkeypatch):
        obj = SpaceApi()
        monkeypatch.setattr(obj, '_content', None)
        monkeypatch.setattr(obj, '_last', None)
        assert obj.outdated is True

        monkeypatch.setattr(obj, '_content', {})
        monkeypatch.setattr(obj, '_last', None)
        assert obj.outdated is True

        past = datetime.utcnow() - timedelta(seconds=2 * SP_API_REFRESH)
        monkeypatch.setattr(obj, '_content', {})
        monkeypatch.setattr(obj, '_last', past)
        assert obj.outdated is True

        monkeypatch.setattr(obj, '_content', {})
        monkeypatch.setattr(obj, '_last', datetime.utcnow())
        assert obj.outdated is False

    @staticmethod
    def test_content_property(monkeypatch):
        obj = SpaceApi()
        content, past = 'something', datetime.utcnow()

        monkeypatch.setattr(obj, 'build', lambda: content)
        assert getattr(obj, '_content', 'error') is None
        assert getattr(obj, '_last', 'error') is None

        assert obj.content == content
        assert getattr(obj, '_content', 'error') == content
        last = getattr(obj, '_last', 'error')
        assert last >= past
        assert last < datetime.utcnow()

    @staticmethod
    def test_update_method(monkeypatch):
        obj = SpaceApi()
        content, past = {'something': 'nice'}, datetime.utcnow()
        state, events = 'broken', ['hardcore', 'party', 'action']

        monkeypatch.setattr(obj, 'build', lambda: content)
        monkeypatch.setattr(obj, 'get_state', lambda: state)
        monkeypatch.setattr(obj, 'get_events', lambda: events)

        assert obj.content == content

        obj.update()

        assert obj.content == dict(state=state, events=events, **content)
        last = getattr(obj, '_last', 'error')
        assert last >= past
        assert last < datetime.utcnow()

    @staticmethod
    def test_reset_method(monkeypatch):
        obj = SpaceApi()
        content, past = {'something': 'nice'}, datetime.utcnow()
        state, events = 'broken', ['hardcore', 'party', 'action']

        monkeypatch.setattr(obj, 'build', lambda: content)
        monkeypatch.setattr(obj, 'get_state', lambda: state)
        monkeypatch.setattr(obj, 'get_events', lambda: events)

        assert getattr(obj, '_content', 'error') is None
        assert getattr(obj, '_last', 'error') is None

        monkeypatch.setattr(obj, '_content', content)
        monkeypatch.setattr(obj, '_last', past)

        assert obj.content == content
        assert getattr(obj, '_content', 'error') == content
        assert getattr(obj, '_last', 'error') == past

        obj.reset()

        assert getattr(obj, '_content', 'error') == dict(
            state=state, events=events, **content
        )
        last = getattr(obj, '_last', 'error')
        assert last >= past
        assert last < datetime.utcnow()
