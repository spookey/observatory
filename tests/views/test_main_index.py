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
    def test_titles(visitor):
        res = visitor(ENDPOINT)
        title = res.soup.select('h1 a.title')[-1]
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        assert title.string.strip() == TITLE
        assert subtitle.string.strip() in TAGLINES

    @staticmethod
    def test_footer(visitor):
        res = visitor(ENDPOINT)
        footer = res.soup.select('footer')[-1]
        assert TITLE in footer.text
