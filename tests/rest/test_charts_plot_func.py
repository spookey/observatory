from collections import namedtuple
from datetime import datetime, timedelta

from flask_restful.fields import Boolean, Float, Integer, String
from pytest import mark

from observatory.lib.clock import epoch_milliseconds
from observatory.models.mapper import EnumConvert, EnumHorizon, Mapper
from observatory.models.point import Point
from observatory.rest.charts import (
    assemble,
    collect_generic,
    collect_points,
    get_value_step_types,
)
from observatory.start.environment import BACKLOG_DAYS


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
            (one_one, s_one),
            (one_two, s_two),
        ]
        assert list(collect_generic(p_two)) == [
            (two_one, s_one),
            (two_two, s_two),
        ]

    @staticmethod
    def test_collect_points_inactive_empty(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor, active=False)

        assert list(collect_points(mapper, sensor)) == []

        mapper.update(active=True)
        assert list(collect_points(mapper, sensor)) == []

    @staticmethod
    def test_collect_points_outdated_empty(gen_prompt, gen_sensor, gen_user):
        prompt, sensor, user = gen_prompt(), gen_sensor(), gen_user()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        start = datetime.utcnow()

        for value in range(5):
            Point.create(
                sensor=sensor,
                user=user,
                value=value,
                created=start - timedelta(days=BACKLOG_DAYS, hours=value),
            )

        assert list(collect_points(mapper, sensor)) == []

    @staticmethod
    def test_collect_points(gen_prompt, gen_sensor, gen_user):
        prompt, sensor, user = gen_prompt(), gen_sensor(), gen_user()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        start = datetime.utcnow()
        two, one, nil = (
            start + timedelta(minutes=2),
            start + timedelta(minutes=1),
            start + timedelta(minutes=0),
        )

        Point.create(sensor=sensor, user=user, created=two, value=13.37)
        Point.create(sensor=sensor, user=user, created=one, value=23)
        Point.create(sensor=sensor, user=user, created=nil, value=0)

        for horizon, convert, params in [
            (
                EnumHorizon.NORMAL,
                EnumConvert.NATURAL,
                [
                    (two, 13.37),
                    (one, 23.0),
                    (nil, 0.0),
                ],
            ),
            (
                EnumHorizon.NORMAL,
                EnumConvert.INTEGER,
                [
                    (two, 13),
                    (one, 23),
                    (nil, 0),
                ],
            ),
            (
                EnumHorizon.NORMAL,
                EnumConvert.BOOLEAN,
                [
                    (two, 1.0),
                    (one, 1.0),
                    (nil, 0.0),
                ],
            ),
            (
                EnumHorizon.INVERT,
                EnumConvert.NATURAL,
                [
                    (two, -13.37),
                    (one, -23.0),
                    (nil, 0),
                ],
            ),
            (
                EnumHorizon.INVERT,
                EnumConvert.INTEGER,
                [
                    (two, -13),
                    (one, -23),
                    (nil, 0),
                ],
            ),
            (
                EnumHorizon.INVERT,
                EnumConvert.BOOLEAN,
                [
                    (two, -1.0),
                    (one, -1.0),
                    (nil, 0.0),
                ],
            ),
        ]:
            mapper.update(horizon=horizon, convert=convert)
            assert list(collect_points(mapper, sensor)) == [
                {'x': epoch_milliseconds(xx), 'y': yy} for xx, yy in params
            ]

    @staticmethod
    def test_assemble_inactive_empty(gen_prompt, gen_sensor):
        prompt, sensor = gen_prompt(), gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor, active=False)

        assert list(assemble(prompt)) == []

        mapper.update(active=True)
        assert list(assemble(prompt)) == []

    @staticmethod
    def test_assemble(gen_prompt, gen_sensor, gen_user):
        prompt, sensor, user = gen_prompt(), gen_sensor(), gen_user()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)
        point = Point.create(sensor=sensor, user=user, value=42)

        expect = namedtuple(
            'ex',
            (
                'value',
                'translated',
                'fill',
                'stepped',
                'tension',
                'value_type',
                'step_type',
            ),
        )

        for horizon, convert, ex in [
            (
                EnumHorizon.NORMAL,
                EnumConvert.NATURAL,
                expect(
                    value=42.0,
                    translated=42.0,
                    fill=True,
                    stepped=False,
                    tension=0.4,
                    value_type=Float,
                    step_type=Boolean,
                ),
            ),
            (
                EnumHorizon.INVERT,
                EnumConvert.INTEGER,
                expect(
                    value=-42,
                    translated=-42,
                    fill=True,
                    stepped=False,
                    tension=0.0,
                    value_type=Integer,
                    step_type=Boolean,
                ),
            ),
            (
                EnumHorizon.INVERT,
                EnumConvert.BOOLEAN,
                expect(
                    value=-1.0,
                    translated=True,
                    fill=False,
                    stepped='before',
                    tension=0.4,
                    value_type=Float,
                    step_type=String,
                ),
            ),
        ]:

            mapper.update(horizon=horizon, convert=convert)

            assert list(assemble(prompt)) == [
                (
                    {
                        'borderColor': mapper.color.color,
                        'data': [
                            {
                                'x': point.created_epoch_ms,
                                'y': ex.value,
                            }
                        ],
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
                                'value': ex.translated,
                            },
                        },
                        'fill': ex.fill,
                        'label': sensor.title,
                        'lineTension': ex.tension,
                        'steppedLine': ex.stepped,
                    },
                    ex.value_type,
                    ex.step_type,
                )
            ]
