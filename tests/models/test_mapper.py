from datetime import datetime

from pytest import mark

from stats.models.mapper import EnumAxis, EnumCast, EnumHorizon, Mapper
from stats.start.environment import FMT_STRFTIME


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
        assert mapper.axis == EnumAxis.LEFT
        assert mapper.cast == EnumCast.NATURAL
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
