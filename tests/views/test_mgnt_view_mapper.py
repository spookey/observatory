from flask import url_for
from pytest import mark

ENDPOINT = 'mgnt.view_mapper'


@mark.usefixtures('session')
class TestMgntViewMapper:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/manage/mapper/view'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_titles(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == 'View mapping'
        assert heading.text.strip() == 'Mapping'

    @staticmethod
    def test_inner_nav(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        tabs = res.soup.select('.tabs li')
        *elements, main = tabs

        assert 'is-active' in main.attrs.get('class')
        assert main.a['href'] == url_for(ENDPOINT)

        for elem in elements:
            assert 'is-active' not in elem.attrs.get('class')
            assert elem.a['href'] in [
                url_for('mgnt.index'),
                url_for('mgnt.view_prompt'),
                url_for('mgnt.view_sensor'),
            ]
