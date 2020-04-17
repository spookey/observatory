from flask import url_for
from pytest import mark

from observatory.models.mapper import Mapper
from observatory.start.environment import ICON, TAGLINES, TITLE

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

    @staticmethod
    def test_empty(visitor):
        res = visitor(ENDPOINT)
        text = res.soup.text

        assert 'nothing there' in text.lower()

    @staticmethod
    def test_view_info(visitor, gen_prompt, gen_sensor):
        prompt = gen_prompt('test_prompt')
        sensor = gen_sensor('test_sensor')
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        point = sensor.append(13.37)

        res = visitor(ENDPOINT)
        text = res.soup.text

        canvas = res.soup.select('canvas')[-1]
        assert canvas is not None
        assert 'chart' in canvas['class']
        assert canvas['data-slug'] == prompt.slug

        assert ICON['glob_descr'] in str(res.soup)

        assert prompt.slug in text
        assert prompt.title in text
        assert prompt.description in text

        assert sensor.slug in text
        assert sensor.title in text
        assert sensor.description in text

        assert point.created_fmt in text
        assert str(point.convert(mapper.convert)) in text
