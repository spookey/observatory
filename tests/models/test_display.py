from pytest import mark

from stats.models.display import Display, EnumAxis, EnumCast, EnumHorizon
from stats.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestDisplay:

    @staticmethod
    def test_default_fields(gen_sensor, gen_config):
        sensor = gen_sensor()
        config = gen_config()

        display = Display.create(
            sensor=sensor, config=config
        )

        assert display.sensor == sensor
        assert display.config == config
        assert display.active is True
        assert display.axis == EnumAxis.LEFT
        assert display.cast == EnumCast.NATURAL
        assert display.horizon == EnumHorizon.NORMAL

    @staticmethod
    def test_created_fmt(gen_sensor, gen_config):
        sensor = gen_sensor()
        config = gen_config()

        display = Display.create(
            sensor=sensor, config=config
        )

        assert display.created_fmt == display.created.strftime(FMT_STRFTIME)
