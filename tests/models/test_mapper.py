from datetime import datetime

from pytest import mark

from observatory.models.mapper import (
    EnumColor,
    EnumConvert,
    EnumHorizon,
    Mapper,
)
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor
from observatory.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestMapper:
    @staticmethod
    def test_default_fields(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()

        mapper = Mapper.create(
            prompt=prompt,
            sensor=sensor,
        )

        assert mapper.prompt == prompt
        assert mapper.sensor == sensor
        assert mapper.active is True
        assert mapper.sortkey == 1
        assert mapper.color == EnumColor.GRAY
        assert mapper.convert == EnumConvert.NATURAL
        assert mapper.horizon == EnumHorizon.NORMAL
        assert mapper.elevate == 1.0

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

        assert (
            mapper.created_epoch
            <= (mapper.created - datetime.utcfromtimestamp(0)).total_seconds()
        )
        assert mapper.created_epoch_ms == 1000 * mapper.created_epoch

    @staticmethod
    def test_mapping_active(gen_prompt, gen_sensor):
        p_one, p_two = gen_prompt('one'), gen_prompt('two')
        s_one, s_two = gen_sensor('one'), gen_sensor('two')
        one_one = Mapper.create(
            prompt=p_one, sensor=s_one, sortkey=4, active=True
        )
        one_two = Mapper.create(
            prompt=p_one, sensor=s_two, sortkey=3, active=False
        )
        two_one = Mapper.create(
            prompt=p_two, sensor=s_one, sortkey=2, active=False
        )
        two_two = Mapper.create(
            prompt=p_two, sensor=s_two, sortkey=1, active=True
        )

        assert p_one.mapping == [one_one, one_two]
        assert p_two.mapping == [two_one, two_two]
        assert s_one.mapping == [one_one, two_one]
        assert s_two.mapping == [one_two, two_two]

        assert p_one.mapping_active == [one_one]
        assert p_two.mapping_active == [two_two]
        assert s_one.mapping_active == [one_one]
        assert s_two.mapping_active == [two_two]

        assert one_one.prompt_active == p_one
        assert one_one.sensor_active == s_one
        assert one_two.prompt_active is None
        assert one_two.sensor_active is None
        assert two_one.prompt_active is None
        assert two_one.sensor_active is None
        assert two_two.prompt_active == p_two
        assert two_two.sensor_active == s_two
