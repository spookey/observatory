from flask import url_for
from flask_restful import marshal
from flask_restful.fields import Boolean, DateTime, Integer, String
from pytest import mark

from observatory.models.mapper import Mapper
from observatory.rest.generic import SlugUrl
from observatory.rest.mapper import MapperSingle

ENDPOINT = 'api.mapper.single'


@mark.usefixtures('session')
class TestMapperSingle:
    @staticmethod
    def test_url():
        assert (
            url_for(
                ENDPOINT, prompt_slug='prompt_test', sensor_slug='sensor_test'
            )
            == '/api/mapper/prompt/prompt_test/sensor/sensor_test'
        )

    @staticmethod
    def test_marshal():
        mdef = MapperSingle.SINGLE_GET
        assert isinstance(mdef['prompt'], String)
        assert isinstance(mdef['sensor'], String)
        assert isinstance(mdef['active'], Boolean)
        created = mdef['created']
        assert isinstance(created, DateTime)
        assert created.dt_format == 'iso8601'
        assert isinstance(mdef['sortkey'], Integer)
        assert isinstance(mdef['color'], String)
        assert isinstance(mdef['convert'], String)
        assert isinstance(mdef['horizon'], String)
        prompt_url = mdef['prompt_url']
        assert isinstance(prompt_url, SlugUrl)
        assert prompt_url.absolute is True
        assert prompt_url.endpoint == 'api.prompt.single'
        sensor_url = mdef['sensor_url']
        assert isinstance(sensor_url, SlugUrl)
        assert sensor_url.absolute is True
        assert sensor_url.endpoint == 'api.sensor.single'

    @staticmethod
    def test_get_empty(visitor):
        res = visitor(
            ENDPOINT,
            params={
                'prompt_slug': 'prompt_test',
                'sensor_slug': 'sensor_test',
            },
            code=404,
        )
        assert 'not present' in res.json['message'].lower()

    @staticmethod
    def test_get_listing(visitor, gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())

        res = visitor(
            ENDPOINT,
            params={
                'prompt_slug': mapper.prompt.slug,
                'sensor_slug': mapper.sensor.slug,
            },
        )
        assert res.json == marshal(mapper, MapperSingle.SINGLE_GET)
