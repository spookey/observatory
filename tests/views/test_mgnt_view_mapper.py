from flask import url_for
from pytest import mark

from observatory.models.mapper import (
    EnumColor, EnumConvert, EnumHorizon, Mapper
)

ENDPOINT = 'mgnt.view_mapper'
ENDINDEX = 'mgnt.index'


@mark.usefixtures('session')
class TestMgntViewMapper:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/manage/mapper/view'
        assert url_for(ENDINDEX) == '/manage'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_titles(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == 'View mapper'
        assert heading.text.strip() == 'Mapper'

    @staticmethod
    def test_empty(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        text = res.soup.text

        assert 'nothing there' in text.lower()

    @staticmethod
    def test_view(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()

        mapper = Mapper.create(
            prompt=gen_prompt(), sensor=gen_sensor(),
            color=EnumColor.BLUE, convert=EnumConvert.INTEGER,
            horizon=EnumHorizon.INVERT,
        )

        res = visitor(ENDPOINT)
        text = res.soup.text

        assert mapper.prompt.slug in text
        assert mapper.sensor.slug in text
        assert mapper.color.name in text
        assert mapper.convert.name in text
        assert mapper.horizon.name in text

    @staticmethod
    def test_inner_nav(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT)
        prompt, mapper, sensor = res.soup.select('.tabs li')

        assert 'is-active' in mapper.attrs.get('class')
        assert mapper.a['href'] == url_for(ENDPOINT)

        for elem, href in (
                (sensor, url_for('mgnt.view_sensor')),
                (prompt, url_for('mgnt.view_prompt')),
        ):
            assert not elem.has_attr('class')
            assert elem.a['href'] == href
