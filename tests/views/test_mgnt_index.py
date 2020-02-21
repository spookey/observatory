from flask import url_for
from pytest import mark

ENDPOINT = 'mgnt.index'


@mark.usefixtures('session')
class TestMgntIndex:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/manage'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_titles(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == 'Management'
        assert heading.text.strip() == 'Overview'

    @staticmethod
    def test_view(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        for elem in res.soup.select('.level'):
            assert elem.select('.heading')[0].text.strip() == 'Type'
            assert elem.select('.title')[-1].text.strip() in [
                'Prompts', 'Sensors', 'Mapping'
            ]
            assert elem.select('.heading')[1].text.strip() == 'Amount'
            assert elem.select('.subtitle')[-1].text.strip() == '0'

    @staticmethod
    def test_inner_nav(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        tabs = res.soup.select('.tabs li')
        main, *elements = tabs

        assert 'is-active' in main.attrs.get('class')
        assert main.a['href'] == url_for(ENDPOINT)

        for elem in elements:
            assert 'is-active' not in elem.attrs.get('class')
            assert elem.a['href'] in [
                url_for('mgnt.view_prompt'),
                url_for('mgnt.view_sensor'),
                url_for('mgnt.view_mapper'),
            ]
