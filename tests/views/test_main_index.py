from flask import url_for
from pytest import mark

from stats.start.environment import TAGLINES, TITLE

ENDPOINT = 'main.index'


@mark.usefixtures('session')
class TestMainIndex:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/'

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_basic_view(visitor):
        res = visitor(ENDPOINT)
        title = res.soup.select('h1 a.title')[-1]
        subtitle = res.soup.select('h2.subtitle')[-1]
        assert title.string == TITLE
        assert subtitle.string in TAGLINES
