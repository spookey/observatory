from flask import url_for
from pytest import mark

from stats.models.mapper import Mapper

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
            assert head.text.strip() in ['Prompts', 'Sensors', 'Mapping']

    @staticmethod
    def test_total_view(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        prompt = gen_prompt()
        sensor = gen_sensor()
        mapper = Mapper.create(prompt=prompt, sensor=sensor)

        res = visitor(ENDPOINT)
        text = res.soup.text

        assert prompt.slug in text
        assert prompt.title in text
        assert prompt.description in text
        assert prompt.created_fmt in text

        assert sensor.slug in text
        assert sensor.title in text
        assert sensor.description in text
        assert sensor.created_fmt in text
        assert 'Points' in text

        assert mapper.created_fmt in text
        assert 'Yes' in text
        assert mapper.axis.name in text
        assert mapper.cast.name in text
        assert mapper.horizon.name in text
