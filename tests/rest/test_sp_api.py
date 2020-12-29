from flask import current_app, url_for
from pytest import mark

ENDPOINT = 'api.sp_api.json'


@mark.usefixtures('session')
class TestSpaceApi:
    @staticmethod
    def test_endpoint():
        assert url_for(ENDPOINT) == '/api/space.json'

    @staticmethod
    def test_disabled(monkeypatch, visitor):
        monkeypatch.setitem(current_app.config, 'ENABLE_SP_API', False)

        res = visitor(ENDPOINT, code=404)
        ctt = res.request.headers.get('content-type', None)
        assert ctt.lower() == 'application/json'

    @staticmethod
    def test_content(visitor):
        res = visitor(ENDPOINT, code=200)
        assert res.json == {}
