from flask import url_for
from pytest import mark

from observatory.models.mapper import Mapper

ENDPOINT = 'api.charts.plot'


@mark.usefixtures('session')
class TestChartsPlot:

    @staticmethod
    def test_url():
        assert url_for(ENDPOINT, slug='demo') == '/api/charts/demo'
        assert url_for(ENDPOINT, slug='') == '/api/charts/'

    @staticmethod
    def test_get_empty(visitor):
        res = visitor(ENDPOINT, params={'slug': 'wrong'}, code=404)
        assert 'not present' in res.json['message'].lower()

    @staticmethod
    def test_get_inactive(visitor, gen_prompt, gen_sensor):
        prompt = gen_prompt()
        Mapper.create(prompt=prompt, sensor=gen_sensor(), active=False)
        res = visitor(ENDPOINT, params={'slug': prompt.slug}, code=410)
        assert 'not active' in res.json['message'].lower()

    @staticmethod
    def test_get_plot(visitor, gen_prompt, gen_sensor):
        prompt = gen_prompt()
        Mapper.create(prompt=prompt, sensor=gen_sensor())
        res = visitor(ENDPOINT, params={'slug': prompt.slug})
        assert prompt.slug in res.json['todo']
