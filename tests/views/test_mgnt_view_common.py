from flask import url_for
from pytest import fixture, mark


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, visitor, gen_prompt, gen_sensor, gen_user_loggedin):
    def res():
        pass

    res.login = gen_user_loggedin
    res.visitor = visitor
    res.endpoint, res.title, res.heading, res.gen_common, res.url = (
        'mgnt.view_prompt', 'View prompts', 'Prompts',
        gen_prompt, '/manage/prompt/view',
    ) if request.param == 'prompt' else (
        'mgnt.view_sensor', 'View sensors', 'Sensors',
        gen_sensor, '/manage/sensor/view',
    )

    yield res


@mark.usefixtures('session')
class TestMgntViewCommon:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url(_comm):
        assert url_for(_comm.endpoint) == _comm.url

    @staticmethod
    def test_no_user(_comm):
        _comm.visitor(_comm.endpoint, code=401)

    @staticmethod
    def test_titles(_comm):
        _comm.login()

        res = _comm.visitor(_comm.endpoint)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == _comm.title
        assert heading.text.strip() == _comm.heading

    @staticmethod
    def test_view(_comm):
        _comm.login()
        thing = _comm.gen_common()

        res = _comm.visitor(_comm.endpoint)
        text = res.soup.text

        assert thing.slug in text
        assert thing.title in text
        assert thing.description in text
        assert thing.created_fmt in text

    @staticmethod
    def test_inner_nav(_comm):
        _comm.login()

        res = _comm.visitor(_comm.endpoint)

        for elem in res.soup.select('.tabs li'):
            if elem.a['href'] == _comm.url:
                assert 'is-active' in elem.attrs.get('class')
            else:
                assert 'is-active' not in elem.attrs.get('class')

            assert elem.a['href'] in [
                url_for('mgnt.index'),
                url_for('mgnt.view_prompt'),
                url_for('mgnt.view_sensor'),
                url_for('mgnt.view_mapper'),
            ]
