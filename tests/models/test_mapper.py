from pytest import mark

from stats.models.mapper import EnumAxis, EnumCast, EnumHorizon, Mapper
from stats.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestMapper:

    @staticmethod
    def test_default_fields(gen_sensor, gen_prompt):
        sensor = gen_sensor()
        prompt = gen_prompt()

        mapper = Mapper.create(
            sensor=sensor, prompt=prompt
        )

        assert mapper.sensor == sensor
        assert mapper.prompt == prompt
        assert mapper.active is True
        assert mapper.axis == EnumAxis.LEFT
        assert mapper.cast == EnumCast.NATURAL
        assert mapper.horizon == EnumHorizon.NORMAL

    @staticmethod
    def test_created_fmt(gen_sensor, gen_prompt):
        sensor = gen_sensor()
        prompt = gen_prompt()

        mapper = Mapper.create(
            sensor=sensor, prompt=prompt
        )

        assert mapper.created_fmt == mapper.created.strftime(FMT_STRFTIME)
