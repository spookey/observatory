from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiLatestValue:
    @staticmethod
    def test_empty():
        api = SpaceApi()

        assert api.latest_value(key='missing', idx=23, convert_key='') is None

    @staticmethod
    def test_empty_points(gen_sensor):
        api = SpaceApi()

        key, idx = 'some.sensor', 42

        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=gen_sensor())

        assert api.latest_value(key=key, idx=idx, convert_key='') is None

    @staticmethod
    def test_empty_options(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 42
        value = 23

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=value)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        assert api.latest_value(key=key, idx=idx, convert_key='') == value

    @staticmethod
    def test_convert(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 23
        convert_key = f'{key}.convert'

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=13.37)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        for convert, expect in [
            ('NATURAL', 13.37),
            ('INTEGER', 13),
            ('BOOLEAN', True),
            (None, 13.37),
            ('banana', 13.37),
        ]:

            Value.set(f'{SP_API_PREFIX}.{convert_key}', idx=idx, elem=convert)
            assert (
                api.latest_value(key=key, idx=idx, convert_key=convert_key)
                == expect
            )
