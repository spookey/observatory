from flask import url_for
from pytest import mark

from observatory.models.mapper import (
    EnumColor,
    EnumConvert,
    EnumHorizon,
    Mapper,
)
from observatory.models.point import Point

ENDPOINT = 'api.charts.plot'


@mark.usefixtures('session')
class TestChartsPlot:
    @staticmethod
    @mark.usefixtures('ctx_app')
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
    def test_get_no_data(visitor, gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        Mapper.create(prompt=prompt, sensor=sensor)

        res = visitor(ENDPOINT, params={'slug': prompt.slug})
        assert res.json == []

    @staticmethod
    def test_get_plot(visitor, gen_prompt, gen_sensor, gen_user):
        user = gen_user()
        prompt = gen_prompt()
        s_one, s_two = gen_sensor('one'), gen_sensor('two')
        m_one = Mapper.create(
            prompt=prompt,
            sensor=s_one,
            color=EnumColor.YELLOW,
            convert=EnumConvert.INTEGER,
            horizon=EnumHorizon.NORMAL,
        )
        m_two = Mapper.create(
            prompt=prompt,
            sensor=s_two,
            color=EnumColor.PURPLE,
            convert=EnumConvert.BOOLEAN,
            horizon=EnumHorizon.INVERT,
        )
        p_one_two = Point.create(sensor=s_one, user=user, value=23.42)
        p_one_one = Point.create(sensor=s_one, user=user, value=1337)
        p_two_two = Point.create(sensor=s_two, user=user, value=42.23)
        p_two_one = Point.create(sensor=s_two, user=user, value=0)

        res = visitor(ENDPOINT, params={'slug': prompt.slug})

        assert res.json == [
            {
                'borderColor': m_two.color.color,
                'data': [
                    {
                        'x': p_two_one.created_epoch_ms,
                        'y': 0.0,
                    },
                    {
                        'x': p_two_two.created_epoch_ms,
                        'y': -1.0,
                    },
                ],
                'display': {
                    'logic': {
                        'color': m_two.color.color,
                        'epoch': p_two_one.created_epoch_ms,
                        'stamp': p_two_one.created_fmt,
                    },
                    'plain': {
                        'convert': m_two.convert.name,
                        'description': s_two.description,
                        'horizon': m_two.horizon.name,
                        'points': 2,
                        'slug': s_two.slug,
                        'title': s_two.title,
                        'value': 'False',
                    },
                },
                'fill': False,
                'label': s_two.title,
                'lineTension': 0.4,
                'steppedLine': 'before',
            },
            {
                'borderColor': m_one.color.color,
                'data': [
                    {
                        'x': p_one_one.created_epoch_ms,
                        'y': 1337,
                    },
                    {
                        'x': p_one_two.created_epoch_ms,
                        'y': 23,
                    },
                ],
                'display': {
                    'logic': {
                        'color': m_one.color.color,
                        'epoch': p_one_one.created_epoch_ms,
                        'stamp': p_one_one.created_fmt,
                    },
                    'plain': {
                        'convert': m_one.convert.name,
                        'description': s_one.description,
                        'horizon': m_one.horizon.name,
                        'points': 2,
                        'slug': s_one.slug,
                        'title': s_one.title,
                        'value': '1337',
                    },
                },
                'fill': True,
                'label': s_one.title,
                'lineTension': 0.0,
                'steppedLine': False,
            },
        ]
