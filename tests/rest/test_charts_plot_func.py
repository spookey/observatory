from datetime import datetime

from flask_restful.fields import Boolean, Float, Integer, String
from pytest import mark

from observatory.models.mapper import EnumConvert, EnumHorizon, Mapper
from observatory.models.point import Point
from observatory.rest.charts import (
    assemble, collect_generic, collect_points, get_value_step_types
)


@mark.usefixtures('session')
class TestChartsPlotFunc:

    @staticmethod
    def test_get_value_step_types(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())

        for convert, expected in (
                (EnumConvert.NATURAL, (Float, Boolean)),
                (EnumConvert.INTEGER, (Integer, Boolean)),
                (EnumConvert.BOOLEAN, (Integer, String)),
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
                    (2000, 1), (1000, 1), (0, 0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.NATURAL, [
                    (2000, -13.37), (1000, -23.0), (0, 0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, [
                    (2000, -13), (1000, -23), (0, 0),
                ]),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, [
                    (2000, -1), (1000, -1), (0, 0),
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

        for horizon, convert, (value, fill, stepped, val_t, stp_t) in [
                (EnumHorizon.NORMAL, EnumConvert.NATURAL, (
                    42.0, True, False, Float, Boolean
                )),
                (EnumHorizon.INVERT, EnumConvert.INTEGER, (
                    -42, True, False, Integer, Boolean
                )),
                (EnumHorizon.INVERT, EnumConvert.BOOLEAN, (
                    -1, False, 'before', Integer, String
                )),
        ]:
            mapper.update(horizon=horizon, convert=convert)
            assert next(assemble(prompt)) == ({
                'borderColor': mapper.color.color,
                'data': [{
                    'x': point.created_epoch_ms,
                    'y': value,
                }],
                'fill': fill,
                'label': sensor.title,
                'steppedLine': stepped,
            }, val_t, stp_t)
