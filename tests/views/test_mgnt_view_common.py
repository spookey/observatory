from flask import url_for
from pytest import fixture, mark

from observatory.models.mapper import Mapper
from observatory.start.environment import ICON


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, visitor, gen_prompt, gen_sensor, gen_user_loggedin):
    def res():
        pass

    res.login = gen_user_loggedin
    res.visitor = visitor
    res.endpoint, res.title, res.heading, res.gen_common, res.url = (
        'mgnt.view_prompt', 'View prompt', 'Prompt',
        gen_prompt, '/manage/prompt/view',
    ) if request.param == 'prompt' else (
        'mgnt.view_sensor', 'View sensor', 'Sensor',
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
    def test_empty(_comm):
        _comm.login()

        res = _comm.visitor(_comm.endpoint)
        text = res.soup.text

        assert 'nothing there' in text.lower()

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
        assert ICON['bool_wrong'] in str(res.soup)

    @staticmethod
    def test_view_map_box(_comm, gen_prompt, gen_sensor):
        _comm.login()

        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        res = _comm.visitor(_comm.endpoint)
        box = res.soup.select('.box')[-1]
        text = box.text

        assert mapper.prompt.slug in text
        assert mapper.sensor.slug in text
        assert mapper.convert.name in text
        assert mapper.horizon.name in text
        assert mapper.color.color in str(box)
        assert ICON['bool_right'] in str(box)

    @staticmethod
    def test_inner_nav(_comm):
        _comm.login()

        res = _comm.visitor(_comm.endpoint)
        prompt, mapper, sensor = res.soup.select('.tabs li')

        assert not mapper.has_attr('class')
        assert mapper.a['href'] == url_for('mgnt.view_mapper')

        for elem, href in (
                (sensor, url_for('mgnt.view_sensor')),
                (prompt, url_for('mgnt.view_prompt')),
        ):
            if elem.a['href'] == _comm.url:
                assert 'is-active' in elem.attrs.get('class')
            else:
                assert not elem.has_attr('class')
            assert elem.a['href'] == href
