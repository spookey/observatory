from pytest import mark

from observatory.logic.space_api import SpaceApi
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


@mark.usefixtures('session')
class TestSpaceApiLatestValue:
    @staticmethod
    def test_empty():
        api = SpaceApi()

        assert (
            api.latest_value(
                key='missing',
                idx=1337,
                horizon_key='',
                convert_key='',
                elevate_key='',
            )
            is None
        )

    @staticmethod
    def test_empty_points(gen_sensor):
        api = SpaceApi()

        key, idx = 'some.sensor', 42

        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=gen_sensor())

        assert (
            api.latest_value(
                key=key,
                idx=idx,
                horizon_key='',
                convert_key='',
                elevate_key='',
            )
            is None
        )

    @staticmethod
    def test_empty_options(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 42
        value = 23

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=value)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        assert (
            api.latest_value(
                key=key,
                idx=idx,
                horizon_key='',
                convert_key='',
                elevate_key='',
            )
            == value
        )

    @staticmethod
    def test_horizon(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 23
        horizon_key = f'{key}.horizon'

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=23)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        for horizon, expect in [
            ('NORMAL', 23),
            ('INVERT', -23),
            (None, 23),
            ('banana', 23),
        ]:

            Value.set(f'{SP_API_PREFIX}.{horizon_key}', idx=idx, elem=horizon)
            assert (
                api.latest_value(
                    key=key,
                    idx=idx,
                    horizon_key=horizon_key,
                    convert_key='',
                    elevate_key='',
                )
                == expect
            )

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
                api.latest_value(
                    key=key,
                    idx=idx,
                    horizon_key='',
                    convert_key=convert_key,
                    elevate_key='',
                )
                == expect
            )

    @staticmethod
    def test_elevate(gen_sensor, gen_user):
        api = SpaceApi()

        key, idx = 'some.sensor', 23
        elevate_key = f'{key}.elevate'

        sensor = gen_sensor()
        sensor.append(user=gen_user(), value=5)
        Value.set(f'{SP_API_PREFIX}.{key}', idx=idx, elem=sensor)

        for elevate, expect in [
            (1, 5),
            (2, 10),
            (-1, -5),
            (None, 5),
            ('banana', 5),
        ]:

            Value.set(f'{SP_API_PREFIX}.{elevate_key}', idx=idx, elem=elevate)
            assert (
                api.latest_value(
                    key=key,
                    idx=idx,
                    horizon_key='',
                    convert_key='',
                    elevate_key=elevate_key,
                )
                == expect
            )
