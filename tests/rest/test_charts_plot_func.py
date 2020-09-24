from collections import namedtuple
from datetime import datetime

from flask_restful.fields import Boolean, Float, Integer, String
from pytest import mark

from observatory.models.mapper import EnumConvert, EnumHorizon, Mapper
from observatory.models.point import Point
from observatory.rest.charts import (
    assemble,
    collect_generic,
    collect_points,
    get_value_step_types,
)


@mark.usefixtures('session')
class TestChartsPlotFunc:

    @staticmethod
    def test_get_value_step_types(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())

        for convert, expected in (
                (EnumConvert.NATURAL, (Float, Boolean)),
                (EnumConvert.INTEGER, (Integer, Boolean)),
                (EnumConvert.BOOLEAN, (Float, String)),
        ):
            mapper.update(convert=convert)
            assert get_value_step_types(mapper) == expected

    @staticmethod
    def test_collect_generic_inactive(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        Mapper.create(prompt=prompt, sensor=gen_sensor(), active=False)

        assert list(collect_generic(prompt)) == []

    @staticmethod
    def test_collect_generic(gen_prompt, gen_sensor):
        p_one, p_two = gen_prompt('one'), gen_prompt('two')
        s_one, s_two = gen_sensor('one'), gen_sensor('two')
        two_two = Mapper.create(prompt=p_two, sensor=s_two)
        two_one = Mapper.create(prompt=p_two, sensor=s_one)
        one_two = Mapper.create(prompt=p_one, sensor=s_two)
        one_one = Mapper.create(prompt=p_one, sensor=s_one)

        assert list(collect_generic(p_one)) == [
            (one_one, s_one), (one_two, s_two)
        ]
        assert list(collect_generic(p_two)) == [
            (two_one, s_one), (two_two, s_two)
        ]

    @staticmethod
    def test_collect_points_inactive_empty(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor, active=False)

        assert list(collect_points(mapper, sensor)) == []

        mapper.update(active=True)
        assert list(collect_points(mapper, sensor)) == []

    @staticmethod
    def test_collect_points(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        Point.create(
            sensor=sensor, created=datetime.utcfromtimestamp(2), value=13.37
        )
        Point.create(
            sensor=sensor, created=datetime.utcfromtimestamp(1), value=23
        )
        Point.create(
            sensor=sensor, created=datetime.utcfromtimestamp(0), value=0
        )

        for horizon, convert, params in [
                (EnumHorizon.NORMAL, EnumConvert.NATURAL, [
                    (2000, 13.37), (1000, 23.0), (0, 0.0),
                ]),
                (EnumHorizon.NORMAL, EnumConvert.INTEGER, [
                    (2000, 13), (1000, 23), (0, 0),
                ]),
                (EnumHorizon.NORMAL, EnumConvert.BOOLEAN, [
                    (2000, 1.0), (1000, 1.0), (0, 0.0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.NATURAL, [
                    (2000, -13.37), (1000, -23.0), (0, 0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, [
                    (2000, -13), (1000, -23), (0, 0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, [
                    (2000, -1.0), (1000, -1.0), (0, 0.0),
                ]),
        ]:
            mapper.update(horizon=horizon, convert=convert)
            assert list(collect_points(mapper, sensor)) == [
                {'x': xx, 'y': yy} for xx, yy in params
            ]

    @staticmethod
    def test_assemble_inactive_empty(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor, active=False)

        assert list(assemble(prompt)) == []

        mapper.update(active=True)
        assert list(assemble(prompt)) == []

    @staticmethod
    def test_assemble(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        point = Point.create(sensor=sensor, value=42)

        expect = namedtuple('ex', (
            'value', 'd_val',
            'fill', 'stepped', 'tension',
            'val_t', 'stp_t',
        ))

        for horizon, convert, ex in [
                (EnumHorizon.NORMAL, EnumConvert.NATURAL, expect(
                    value=42.0, d_val=42.0,
                    fill=True, stepped=False, tension=0.4,
                    val_t=Float, stp_t=Boolean
                )),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, expect(
                    value=-42, d_val=-42,
                    fill=True, stepped=False, tension=0.0,
                    val_t=Integer, stp_t=Boolean
                )),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, expect(
                    value=-1.0, d_val=True,
                    fill=False, stepped='before', tension=0.4,
                    val_t=Float, stp_t=String
                )),
        ]:

            mapper.update(horizon=horizon, convert=convert)

            assert list(assemble(prompt)) == [({
                'borderColor': mapper.color.color,
                'data': [{
                    'x': point.created_epoch_ms,
                    'y': ex.value,
                }],
                'display': {
                    'logic': {
                        'color': mapper.color.color,
                        'epoch': point.created_epoch_ms,
                        'stamp': point.created_fmt,
                    },
                    'plain': {
                        'convert': convert.name,
                        'description': sensor.description,
                        'horizon': horizon.name,
                        'points': 1,
                        'slug': sensor.slug,
                        'title': sensor.title,
                        'value': ex.d_val,
                    },
                },
                'fill': ex.fill,
                'label': sensor.title,
                'lineTension': ex.tension,
                'steppedLine': ex.stepped,
            }, ex.val_t, ex.stp_t)]
