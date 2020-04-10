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
        'mgnt.drop_prompt', 'mgnt.view_prompt',
        Prompt, gen_prompt, '/manage/prompt/drop',
    ) if request.param == 'prompt' else (
        'mgnt.drop_sensor', 'mgnt.view_sensor',
        Sensor, gen_sensor, '/manage/sensor/drop',
    )

    yield res


@mark.usefixtures('session')
class TestMgntDropCommon:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url(_comm):
        assert url_for(_comm.endpoint, slug='test') == f'{_comm.url}/test'

    @staticmethod
    def test_no_user(_comm):
        _comm.visitor(_comm.endpoint, method='post', params={
            'slug': 'slug'
        }, code=401)

    @staticmethod
    def test_form_params(_comm):
        _comm.login()
        thing = _comm.gen_common()
        res = _comm.visitor(_comm.view_ep)

        form = res.soup.select('form')[-1]
        assert form['method'] == 'POST'
        assert form['action'] == url_for(
            _comm.endpoint, slug=thing.slug, _external=True
        )

    @staticmethod
    def test_form_fields(_comm):
        _comm.login()
        _comm.gen_common()
        res = _comm.visitor(_comm.view_ep)

        form = res.soup.select('form')[-1]
        fields = [
            (inp.attrs.get('name'), inp.attrs.get('type'))
            for inp in form.select('button')
        ]
        assert fields == [
            ('submit', 'submit'),
        ]

    @staticmethod
    def test_form_no_slug(_comm):
        _comm.login()
        slug = '🐢'

        res = _comm.visitor(_comm.endpoint, method='post', params={
            'slug': slug,
        }, code=500)

        message = f'no such {_comm.model.__name__}'
        assert message.lower() in res.soup.text.lower()

    @staticmethod
    def test_form_deletes(_comm):
        _comm.login()
        thing = _comm.gen_common()
        view_url = url_for(_comm.view_ep, _external=True)

        assert _comm.model.query.all() == [thing]
        res = _comm.visitor(_comm.endpoint, method='post', params={
            'slug': thing.slug,
        }, code=302)

        assert res.request.headers['LOCATION'] == view_url
        assert _comm.model.query.all() == []
