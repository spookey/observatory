from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.mapper import EnumConvert
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiLatestValue:
    @staticmethod
    def test_empty():
        api = SpaceApi()

        assert (
            api.latest_value(
                key='missing', idx=23, convert=EnumConvert.BOOLEAN
            )
            is None
        )

    @staticmethod
    def test_empty_points(gen_sensor):
        api = SpaceApi()

        key, idx = 'some.sensor', 42

        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=gen_sensor())

        assert (
            api.latest_value(key=key, idx=idx, convert=EnumConvert.INTEGER)
            is None
        )

    @staticmethod
    def test_conversion(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 23

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=13.37)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        for convert, expect in [
            (EnumConvert.NATURAL, 13.37),
            (EnumConvert.INTEGER, 13),
            (EnumConvert.BOOLEAN, True),
        ]:

            assert (
                api.latest_value(key=key, idx=idx, convert=convert) == expect
            )
