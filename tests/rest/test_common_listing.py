from flask import url_for
from flask_restful import fields, marshal
from pytest import fixture, mark

from stats.rest.prompt import PromptListing
from stats.rest.sensor import SensorListing


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.endpoint, res.single_ep, res.url, res.gen, res.impl = (
        'api.prompt.listing', 'api.prompt.single', '/api/prompt',
        gen_prompt, PromptListing,
    ) if request.param == 'prompt' else (
        'api.sensor.listing', 'api.sensor.single', '/api/sensor',
        gen_sensor, SensorListing,
    )

    yield res


@mark.usefixtures('session')
class TestCommonListing:

    @staticmethod
    def test_endpoint(_comm):
        assert url_for(_comm.endpoint) == _comm.url

    @staticmethod
    def test_marshal(_comm):
        mdef = _comm.impl.LISTING_GET
        assert isinstance(mdef['slug'], fields.String)
        assert isinstance(mdef['title'], fields.String)
        assert isinstance(mdef['description'], fields.String)
        created = mdef['created']
        assert isinstance(created, fields.DateTime)
        assert created.dt_format == 'iso8601'
        single = mdef['single']
        assert isinstance(single, fields.Url)
        assert single.absolute is True
        assert single.endpoint == _comm.single_ep

    @staticmethod
    def test_get_empty(_comm, visitor):
        res = visitor(_comm.endpoint)
        assert res.json == []

    @staticmethod
    def test_get_listing(_comm, visitor):
        common = [
            _comm.gen(slug='one'), _comm.gen(slug='two'),
        ]
        res = visitor(_comm.endpoint)
        assert res.json == marshal(common, _comm.impl.LISTING_GET)
