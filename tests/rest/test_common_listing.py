from flask import url_for
from flask_restful import marshal
from flask_restful.fields import String, Url
from pytest import fixture, mark

from observatory.rest.prompt import PromptListing
from observatory.rest.sensor import SensorListing


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
        assert isinstance(mdef['slug'], String)
        assert isinstance(mdef['title'], String)
        url = mdef['url']
        assert isinstance(url, Url)
        assert url.absolute is True
        assert url.endpoint == _comm.single_ep

    @staticmethod
    def test_get_empty(_comm, visitor):
        res = visitor(_comm.endpoint)
        assert res.json == []

    @staticmethod
    def test_get_listing(_comm, visitor):
        one = _comm.gen(slug='one')
        two = _comm.gen(slug='two')
        commons = [two, one]  # newest first, query is sorted
        res = visitor(_comm.endpoint)
        assert res.json == marshal(commons, _comm.impl.LISTING_GET)
