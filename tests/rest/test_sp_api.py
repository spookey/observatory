from flask import current_app, url_for
from pytest import mark

ENDPOINT = 'api.sp_api.json'


@mark.usefixtures('session')
class TestSpaceApi:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_endpoint():
        assert url_for(ENDPOINT) == '/api/space.json'

    @staticmethod
    def test_disabled(monkeypatch, visitor):
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)

        res = visitor(ENDPOINT, code=404)
        ctt = res.request.headers.get('content-type', None)
        assert ctt.lower() == 'application/json'

    @staticmethod
    def test_empty_content(visitor):
        res = visitor(ENDPOINT, code=202)
        assert res.json == {
            'api_compatibility': ['14'],
            'space': '',
            'logo': '',
            'url': '',
            'location': {'lat': 0, 'lon': 0},
            'contact': {},
        }
