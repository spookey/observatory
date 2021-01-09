from flask import current_app, url_for
from flask.json import dumps
from pytest import mark

from observatory.instance import SPACE_API

ENDPOINT = 'sapi.index'


@mark.usefixtures('session')
class TestSapiIndex:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/space'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_disabled(monkeypatch, visitor, gen_user_loggedin):
        gen_user_loggedin()
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)

        visitor(ENDPOINT, code=404)

    @staticmethod
    def test_titles(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == 'Space API'
        assert heading.text.strip() == 'Space API'

    @staticmethod
    def test_content_display(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        box = res.soup.select('div.is-one-third pre code')[-1]

        assert box.text == dumps(SPACE_API.content, indent=2, sort_keys=True)

    @staticmethod
    def test_content_headings(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        col = res.soup.select('div.is-two-thirds')[-1]

        headings = col.select('h3.subtitle')

        assert [head.text.strip() for head in headings] == [
            'Info',
            'Location',
            'SpaceFED',
            'Cam',
            'State icons',
            'Contact',
            'Keymasters',
            'Temperature sensor',
            'Door locked sensor',
            'Barometer',
            'Humidity sensor',
            'Beverage supply',
            'Power consumption',
            'Account balance',
            'Blog feed',
            'Wiki feed',
            'Calendar feed',
            'Flickr feed',
            'Projects',
            'Links',
            'Membership plans',
        ]
