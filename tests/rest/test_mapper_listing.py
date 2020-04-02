from flask import url_for
from flask_restful import marshal
from flask_restful.fields import Boolean, String, Url
from pytest import mark

from stats.models.mapper import Mapper
from stats.rest.mapper import MapperListing

ENDPOINT = 'api.mapper.listing'


@mark.usefixtures('session')
class TestMapperListing:

    @staticmethod
    def test_endpoint():
        assert url_for(ENDPOINT) == '/api/mapper'

    @staticmethod
    def test_marshal():
        mdef = MapperListing.LISTING_GET
        assert isinstance(mdef['prompt'], String)
        assert isinstance(mdef['sensor'], String)
        assert isinstance(mdef['active'], Boolean)
        url = mdef['url']
        assert isinstance(url, Url)
        assert url.absolute is True
        assert url.endpoint == 'api.mapper.single'

    @staticmethod
    def test_get_empty(visitor):
        res = visitor(ENDPOINT)
        assert res.json == []

    @staticmethod
    def test_get_listing(visitor, gen_prompt, gen_sensor):
        mappers = [
            Mapper.create(prompt=gen_prompt('one'), sensor=gen_sensor('one')),
            Mapper.create(prompt=gen_prompt('two'), sensor=gen_sensor('two')),
        ]
        res = visitor(ENDPOINT)
        assert res.json == marshal(mappers, MapperListing.LISTING_GET)