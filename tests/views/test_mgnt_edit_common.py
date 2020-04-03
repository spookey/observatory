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
        'mgnt.edit_prompt', 'mgnt.view_prompt',
        Prompt, gen_prompt, '/manage/prompt/edit',
    ) if request.param == 'prompt' else (
        'mgnt.edit_sensor', 'mgnt.view_sensor',
        Sensor, gen_sensor, '/manage/sensor/edit',
    )

    yield res


@mark.usefixtures('session')
class TestMgntEditCommon:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url(_comm):
        assert url_for(_comm.endpoint) == _comm.url
        assert url_for(_comm.endpoint, slug='test') == f'{_comm.url}/test'

    @staticmethod
    def test_no_user(_comm):
        _comm.visitor(_comm.endpoint, code=401)

    @staticmethod
    def test_form_params(_comm):
        _comm.login()
        res = _comm.visitor(_comm.endpoint)

        form = res.soup.select('form')[-1]
        assert form['method'] == 'POST'
        assert form['action'] == url_for(_comm.endpoint, _external=True)

    @staticmethod
    def test_form_fields(_comm):
        _comm.login()
        res = _comm.visitor(_comm.endpoint)

        form = res.soup.select('form')[-1]
        fields = [
            (inp.attrs.get('name'), inp.attrs.get('type', '_ta_'))
            for inp in form.select('input,textarea')
        ]
        assert fields == [
            ('slug', 'text'),
            ('title', 'text'),
            ('description', '_ta_'),
            ('submit', 'submit'),
        ]

    @staticmethod
    def test_form_wrong(_comm):
        _comm.login()
        slug = '🦏'
        title = ''
        description = 'Wrong!'

        res = _comm.visitor(_comm.endpoint, method='post', data={
            'slug': slug, 'title': title,
            'description': description, 'submit': True,
        })

        form = res.soup.select('form')[-1]
        assert form.select('#slug')[-1].attrs['value'] == slug
        assert form.select('#title')[-1].attrs['value'] == title
        assert form.select('#description')[-1].string == description
        assert _comm.model.query.all() == []

    @staticmethod
    def test_form_creates(_comm):
        _comm.login()
        slug = 'my_common'
        title = 'My common'
        description = 'This is my common!'
        view_url = url_for(_comm.view_ep, _external=True)

        res = _comm.visitor(_comm.endpoint, method='post', data={
            'slug': slug, 'title': title,
            'description': description, 'submit': True,
        }, code=302)

        assert res.request.headers['LOCATION'] == view_url
        thing = _comm.model.query.first()
        assert thing.slug == slug
        assert thing.title == title
        assert thing.description == description

    @staticmethod
    def test_form_changes(_comm):
        _comm.login()
        original = _comm.gen_common()

        slug = 'my_common'
        title = 'My common'
        description = 'This is my common!'

        _comm.visitor(_comm.endpoint, params={
            'slug': original.slug
        }, method='post', data={
            'slug': slug, 'title': title,
            'description': description, 'submit': True
        }, code=302)

        changed = _comm.model.query.first()
        assert changed == original
        assert changed.slug == slug
        assert changed.title == title
        assert changed.description == description
