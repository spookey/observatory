from datetime import datetime
from uuid import UUID

from pytest import mark

from observatory.models.mapper import EnumCast, EnumColor, EnumHorizon, Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor
from observatory.start.environment import FMT_STRFTIME

U_ONE = UUID('11111111-1111-4111-1111-111111111111')
U_TWO = UUID('22222222-2222-4222-2222-222222222222')
U_THR = UUID('33333333-3333-4333-3333-333333333333')


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
        assert mapper.cast == EnumCast.NATURAL
        assert mapper.color == EnumColor.GRAY
        assert mapper.horizon == EnumHorizon.NORMAL

        assert isinstance(mapper.sortkey, UUID)

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
        mapper = Mapper.create(
            prompt=gen_prompt(),
            sensor=gen_sensor(),
        )

        assert mapper.created_fmt == mapper.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_created_epoch(gen_prompt, gen_sensor):
        mapper = Mapper.create(
            prompt=gen_prompt(),
            sensor=gen_sensor(),
        )

        assert mapper.created_epoch <= (
            mapper.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert mapper.created_epoch_ms == 1000 * mapper.created_epoch

    @staticmethod
    def test_query_sorted(gen_prompt, gen_sensor):
        m_thr = Mapper.create(
            sortkey=U_THR,
            prompt=gen_prompt('thr'), sensor=gen_sensor('thr')
        )
        m_two = Mapper.create(
            sortkey=U_TWO,
            prompt=gen_prompt('two'), sensor=gen_sensor('two')
        )
        m_one = Mapper.create(
            sortkey=U_ONE,
            prompt=gen_prompt('one'), sensor=gen_sensor('one')
        )
        assert Mapper.query.all() == [m_thr, m_two, m_one]
        assert Mapper.query_sorted().all() == [m_one, m_two, m_thr]

    @staticmethod
    def test_above_below(gen_prompt, gen_sensor):
        p_one = gen_prompt('one')
        p_two = gen_prompt('two')
        s_one = gen_sensor('one')
        s_two = gen_sensor('two')
        m_one = Mapper.create(sortkey=U_ONE, prompt=p_one, sensor=s_one)
        m_two = Mapper.create(sortkey=U_TWO, prompt=p_one, sensor=s_two)
        m_thr = Mapper.create(sortkey=U_THR, prompt=p_two, sensor=s_two)

        assert m_one.query_above().all() == [m_two, m_thr]
        assert m_one.query_below().all() == []
        assert m_two.query_above().all() == [m_thr]
        assert m_two.query_below().all() == [m_one]
        assert m_thr.query_above().all() == []
        assert m_thr.query_below().all() == [m_one, m_two]

        qp_one = Mapper.query.filter(Mapper.prompt == p_one)
        assert m_one.query_above(qp_one).all() == [m_two]
        assert m_one.query_below(qp_one).all() == []
        assert m_two.query_above(qp_one).all() == []
        assert m_two.query_below(qp_one).all() == [m_one]
        assert m_thr.query_above(qp_one).all() == []
        assert m_thr.query_below(qp_one).all() == [m_one, m_two]

        qp_two = Mapper.query.filter(Mapper.prompt == p_two)
        assert m_one.query_above(qp_two).all() == [m_thr]
        assert m_one.query_below(qp_two).all() == []
        assert m_two.query_above(qp_two).all() == [m_thr]
        assert m_two.query_below(qp_two).all() == []
        assert m_thr.query_above(qp_two).all() == []
        assert m_thr.query_below(qp_two).all() == []

        qs_one = Mapper.query.filter(Mapper.sensor == s_one)
        assert m_one.query_above(qs_one).all() == []
        assert m_one.query_below(qs_one).all() == []
        assert m_two.query_above(qs_one).all() == []
        assert m_two.query_below(qs_one).all() == [m_one]
        assert m_thr.query_above(qs_one).all() == []
        assert m_thr.query_below(qs_one).all() == [m_one]

        qs_two = Mapper.query.filter(Mapper.sensor == s_two)
        assert m_one.query_above(qs_two).all() == [m_two, m_thr]
        assert m_one.query_below(qs_two).all() == []
        assert m_two.query_above(qs_two).all() == [m_thr]
        assert m_two.query_below(qs_two).all() == []
        assert m_thr.query_above(qs_two).all() == []
        assert m_thr.query_below(qs_two).all() == [m_two]
