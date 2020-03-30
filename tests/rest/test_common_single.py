from flask import url_for
from flask_restful import marshal
from pytest import fixture, mark

from stats.rest.prompt import PromptSingle
from stats.rest.sensor import SensorSingle


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.endpoint, res.url, res.gen, res.impl = (
        'api.prompt.single', '/api/prompt',
        gen_prompt, PromptSingle,
    ) if request.param == 'prompt' else (
        'api.sensor.single', '/api/sensor',
        gen_sensor, SensorSingle,
    )

    yield res


@mark.usefixtures('session')
class TestCommonSingle:

    @staticmethod
    def test_url(_comm):
        assert url_for(_comm.endpoint, slug='test') == f'{_comm.url}/test'

    @staticmethod
    def test_get_empty(_comm, visitor):
        res = visitor(_comm.endpoint, params={'slug': 'wrong'}, code=404)
        err = res.json.get('error', None)
        assert err
        assert 'not present' in err.lower()

    @staticmethod
    def test_get_single(_comm, visitor):
        common = _comm.gen()

        res = visitor(_comm.endpoint, params={'slug': common.slug})
        assert res.json == marshal(common, _comm.impl.SINGLE_GET)
