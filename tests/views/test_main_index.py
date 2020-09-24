from flask import url_for
from pytest import mark

from observatory.models.mapper import Mapper
from observatory.start.environment import ICON, TAGLINES, TITLE

ENDPOINT = 'main.index'


@mark.usefixtures('session')
class TestMainIndex:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_urls():
        assert url_for(ENDPOINT) == '/'
        assert url_for(ENDPOINT, slug='test') == '/show/test'

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
    def test_single_none(visitor):
        visitor(ENDPOINT, params={'slug': 'none'}, code=404)

    @staticmethod
    def test_single_view(visitor, gen_prompt, gen_sensor):
        prompt = gen_prompt('test_prompt')
        sensor = gen_sensor('test_sensor')
        Mapper.create(prompt=prompt, sensor=sensor)
        sensor.append(13.37)

        res = visitor(ENDPOINT, params={'slug': prompt.slug})
        text = res.soup.text

        assert prompt.slug in text
        assert prompt.title in text
        assert prompt.description in text

    @staticmethod
    def test_view_info(visitor, gen_prompt, gen_sensor):
        prompt_one = gen_prompt('prompt_one')
        prompt_two = gen_prompt('prompt_two')
        sensor_one = gen_sensor('sensor_one')
        sensor_two = gen_sensor('sensor_two')
        Mapper.create(prompt=prompt_two, sensor=sensor_one)
        Mapper.create(prompt=prompt_one, sensor=sensor_two)
        sensor_one.append(23)
        sensor_two.append(42)

        res = visitor(ENDPOINT)
        text = res.soup.text

        assert prompt_one.slug in text
        assert prompt_two.slug in text
        assert prompt_one.title in text
        assert prompt_two.title in text
        assert prompt_one.description in text
        assert prompt_one.description in text

        assert ICON['glob_descr'] in str(res.soup)

        (plot_two, plot_one) = res.soup.select('.plot')
        assert plot_one['data-slug'] == prompt_one.slug
        assert plot_two['data-slug'] == prompt_two.slug

        for plot in (plot_one, plot_two):
            assert plot.select('canvas')[-1] is not None
            assert plot.select('progress')[-1] is not None
            assert plot.select('template')[-1] is not None
            assert plot.select('.control-buttons')[-1] is not None
            assert plot.select('.bucket')[-1] is not None
