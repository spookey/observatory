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
        assert heading.text.strip() == 'Sensors'

    @staticmethod
    def test_sensor_view(visitor, gen_user_loggedin, gen_sensor):
        gen_user_loggedin()
        sensor = gen_sensor()
        res = visitor(ENDPOINT)
        text = res.soup.text
        assert sensor.slug in text
        assert sensor.title in text
        assert sensor.description in text
        assert 'Points' in text
