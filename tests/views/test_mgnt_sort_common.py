from flask import url_for
from pytest import fixture, mark

from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, visitor, gen_prompt, gen_sensor, gen_user_loggedin):
    def res():
        pass

    res.login = gen_user_loggedin
    res.visitor = visitor
    res.endpoint, res.view_ep, res.model, res.gen_common, res.url = (
        'mgnt.sort_prompt', 'mgnt.view_prompt',
        Prompt, gen_prompt, '/manage/prompt/sort',
    ) if request.param == 'prompt' else (
        'mgnt.sort_sensor', 'mgnt.view_sensor',
        Sensor, gen_sensor, '/manage/sensor/sort',
    )

    yield res


@mark.usefixtures('session')
class TestMgntSortCommon:

    @staticmethod
    @mark.usefixtures('ctx_app')
    @mark.parametrize('direction', ['raise', 'lower'])
    def test_url(_comm, direction):
        assert url_for(
            _comm.endpoint, slug='test', direction=direction
        ) == f'{_comm.url}/test/{direction}'

    @staticmethod
    def test_no_user(_comm):
        _comm.visitor(_comm.endpoint, method='post', params={
            'slug': 'slug', 'direction': 'lower',
        }, code=401)

    @staticmethod
    def test_form_no_slug(_comm):
        _comm.login()
        slug = '🐇'

        res = _comm.visitor(_comm.endpoint, method='post', params={
            'slug': slug, 'direction': 'raise',
        }, code=500)

        name = _comm.model.__name__.lower()
        assert f'no such {name}' in res.soup.text.lower()

    @staticmethod
    def test_form_sorts(_comm):
        _comm.login()
        one = _comm.gen_common('one', sortkey=1)
        two = _comm.gen_common('two', sortkey=2)

        view_url = url_for(_comm.view_ep, _external=True)

        def _order(thing, lift):
            res = _comm.visitor(_comm.endpoint, method='post', params={
                'slug': thing.slug,
                'direction': 'raise' if lift else 'lower',
            }, code=302)

            assert res.request.headers['LOCATION'] == view_url
            return _comm.model.query_sorted().all()

        assert _comm.model.query_sorted().all() == [two, one]

        assert _order(one, True) == [one, two]
        assert _order(one, False) == [two, one]
        assert _order(two, False) == [one, two]
        assert _order(two, True) == [two, one]

        assert _order(two, True) == [two, one]
        assert _order(one, False) == [two, one]
