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
        headings = res.soup.select('h3.title')
        assert subtitle.text.strip() == 'Management'
        for head in headings:
            assert head.text.strip() in ['Prompts', 'Sensors']

    @staticmethod
    def test_sensor_view(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        prompt = gen_prompt()
        sensor = gen_sensor()
        res = visitor(ENDPOINT)
        text = res.soup.text

        assert prompt.slug in text
        assert prompt.title in text
        assert prompt.description in text

        assert sensor.slug in text
        assert sensor.title in text
        assert sensor.description in text
        assert 'Points' in text
