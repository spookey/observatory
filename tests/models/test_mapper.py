from datetime import datetime

from pytest import fixture, mark

from observatory.models.mapper import (
    EnumColor, EnumConvert, EnumHorizon, Mapper
)
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor
from observatory.start.environment import FMT_STRFTIME


@fixture(scope='function')
def _make_simple(gen_prompt, gen_sensor):
    def res():
        return (
            Mapper.create(
                sortkey=3, prompt=gen_prompt('thr'), sensor=gen_sensor('thr')
            ),
            Mapper.create(
                sortkey=2, prompt=gen_prompt('two'), sensor=gen_sensor('two')
            ),
            Mapper.create(
                sortkey=1, prompt=gen_prompt('one'), sensor=gen_sensor('one')
            ),
        )

    yield res


@fixture(scope='function')
def _make_nested(gen_prompt, gen_sensor):
    p_one = gen_prompt('one')
    p_two = gen_prompt('two')
    s_one = gen_sensor('one')
    s_two = gen_sensor('two')

    def res():
        return (
            p_one, p_two,
            s_one, s_two,
            Mapper.create(sortkey=1, prompt=p_one, sensor=s_one),
            Mapper.create(sortkey=2, prompt=p_one, sensor=s_two),
            Mapper.create(sortkey=3, prompt=p_two, sensor=s_two),
        )

    yield res


@mark.usefixtures('session')
class TestMapper:

    @staticmethod
    def test_default_fields(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()

        mapper = Mapper.create(
            prompt=prompt, sensor=sensor,
        )

        assert mapper.prompt == prompt
        assert mapper.sensor == sensor
        assert mapper.active is True
        assert mapper.sortkey is not None
        assert mapper.color == EnumColor.GRAY
        assert mapper.convert == EnumConvert.NATURAL
        assert mapper.horizon == EnumHorizon.NORMAL

    @staticmethod
    def test_by_commons(gen_prompt, gen_sensor):
        p_one = gen_prompt(slug='one')
        s_one = gen_sensor(slug='one')
        p_two = gen_prompt(slug='two')
        s_two = gen_sensor(slug='two')

        one = Mapper.create(prompt=p_one, sensor=s_one)
        two = Mapper.create(prompt=p_two, sensor=s_two)

        assert Mapper.query.all() == [one, two]

        assert Mapper.by_commons(p_one, s_one) == one
        assert Mapper.by_commons(p_two, s_two) == two
        assert Mapper.by_commons(p_one, s_two) is None
        assert Mapper.by_commons(p_two, s_one) is None

    @staticmethod
    def test_delete_cascade(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)

        assert Mapper.query.all() == [mapper]
        assert prompt.mapping == [mapper]
        assert sensor.mapping == [mapper]

        assert mapper.delete()

        assert prompt.mapping == []
        assert sensor.mapping == []
        assert Mapper.query.all() == []

    @staticmethod
    def test_delete_cascade_orphan(gen_prompt, gen_sensor):
        for name in ['prompt', 'sensor']:
            mapper = Mapper.create(
                prompt=gen_prompt(slug=f'test_{name}'),
                sensor=gen_sensor(slug=f'test_{name}'),
            )

            assert Mapper.query.all() == [mapper]
            assert getattr(mapper, name).delete()
            assert Mapper.query.all() == []

        assert Prompt.query.count() == 1
        assert Sensor.query.count() == 1
        assert Prompt.query.first().slug == 'test_sensor'
        assert Sensor.query.first().slug == 'test_prompt'

    @staticmethod
    def test_created_fmt(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        assert mapper.created_fmt == mapper.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_created_epoch(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())

        assert mapper.created_epoch <= (
            mapper.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert mapper.created_epoch_ms == 1000 * mapper.created_epoch

    @staticmethod
    def test_query_sorted(_make_simple):
        thr, two, one = _make_simple()

        assert Mapper.query.all() == [thr, two, one]
        assert Mapper.query_sorted().all() == [one, two, thr]

    @staticmethod
    def test_above_below(_make_nested):
        p_one, p_two, s_one, s_two, one_one, one_two, two_two = _make_nested()
        assert Mapper.query_sorted().all() == [one_one, one_two, two_two]

        assert one_one.query_above().all() == [one_two, two_two]
        assert one_one.query_below().all() == []
        assert one_two.query_above().all() == [two_two]
        assert one_two.query_below().all() == [one_one]
        assert two_two.query_above().all() == []
        assert two_two.query_below().all() == [one_one, one_two]

        qp_one = Mapper.query.filter(Mapper.prompt == p_one)
        assert one_one.query_above(qp_one).all() == [one_two]
        assert one_one.query_below(qp_one).all() == []
        assert one_two.query_above(qp_one).all() == []
        assert one_two.query_below(qp_one).all() == [one_one]
        assert two_two.query_above(qp_one).all() == []
        assert two_two.query_below(qp_one).all() == [one_one, one_two]

        qp_two = Mapper.query.filter(Mapper.prompt == p_two)
        assert one_one.query_above(qp_two).all() == [two_two]
        assert one_one.query_below(qp_two).all() == []
        assert one_two.query_above(qp_two).all() == [two_two]
        assert one_two.query_below(qp_two).all() == []
        assert two_two.query_above(qp_two).all() == []
        assert two_two.query_below(qp_two).all() == []

        qs_one = Mapper.query.filter(Mapper.sensor == s_one)
        assert one_one.query_above(qs_one).all() == []
        assert one_one.query_below(qs_one).all() == []
        assert one_two.query_above(qs_one).all() == []
        assert one_two.query_below(qs_one).all() == [one_one]
        assert two_two.query_above(qs_one).all() == []
        assert two_two.query_below(qs_one).all() == [one_one]

        qs_two = Mapper.query.filter(Mapper.sensor == s_two)
        assert one_one.query_above(qs_two).all() == [one_two, two_two]
        assert one_one.query_below(qs_two).all() == []
        assert one_two.query_above(qs_two).all() == [two_two]
        assert one_two.query_below(qs_two).all() == []
        assert two_two.query_above(qs_two).all() == []
        assert two_two.query_below(qs_two).all() == [one_two]

    @staticmethod
    def test_raise_lower_step(_make_simple):
        thr, two, one = _make_simple()

        assert Mapper.query.all() == [thr, two, one]
        assert Mapper.query_sorted().all() == [one, two, thr]

        assert one.raise_step() is True
        assert Mapper.query_sorted().all() == [two, one, thr]

        assert one.raise_step() is True
        assert Mapper.query_sorted().all() == [two, thr, one]

        assert one.raise_step() is False
        assert Mapper.query_sorted().all() == [two, thr, one]

        assert two.raise_step() is True
        assert Mapper.query_sorted().all() == [thr, two, one]

        assert one.lower_step() is True
        assert Mapper.query_sorted().all() == [thr, one, two]

        assert one.lower_step() is True
        assert Mapper.query_sorted().all() == [one, thr, two]

        assert one.lower_step() is False
        assert Mapper.query_sorted().all() == [one, thr, two]

        assert two.lower_step() is True
        assert Mapper.query_sorted().all() == [one, two, thr]

    @staticmethod
    def test_raise_lower_keeps_others(_make_nested):
        p_one, p_two, s_one, s_two, one_one, one_two, two_two = _make_nested()
        qp_one = Mapper.query.filter(Mapper.prompt == p_one)
        qp_two = Mapper.query.filter(Mapper.prompt == p_two)
        qs_one = Mapper.query.filter(Mapper.sensor == s_one)
        qs_two = Mapper.query.filter(Mapper.sensor == s_two)

        def _verify(prompt_flip, sensor_flip):
            assert Mapper.query_sorted(qp_one).all() == (
                [one_two, one_one] if prompt_flip else [one_one, one_two]
            )
            assert Mapper.query_sorted(qp_two).all() == [two_two]
            assert Mapper.query_sorted(qs_one).all() == [one_one]
            assert Mapper.query_sorted(qs_two).all() == (
                [two_two, one_two] if sensor_flip else [one_two, two_two]
            )

        assert Mapper.query_sorted().all() == [one_one, one_two, two_two]
        _verify(False, False)

        assert one_one.raise_step() is True
        assert Mapper.query_sorted().all() == [one_two, one_one, two_two]
        _verify(True, False)

        assert one_one.raise_step() is True
        assert Mapper.query_sorted().all() == [one_two, two_two, one_one]
        _verify(True, False)

        assert one_two.raise_step() is True
        assert Mapper.query_sorted().all() == [two_two, one_two, one_one]
        _verify(True, True)
