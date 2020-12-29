from flask import url_for
from pytest import mark

from observatory.models.point import Point
from observatory.start.environment import ICON

ENDPOINT = 'user.home'


@mark.usefixtures('session')
class TestUser:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/user'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_titles(visitor, gen_user_loggedin):
        user = gen_user_loggedin()

        res = visitor(ENDPOINT)
        subtitle = res.soup.select('h2 a.subtitle')[-1]
        heading = res.soup.select('h3.title')[-1]
        assert subtitle.text.strip() == 'Welcome home!'
        assert heading.text.strip() == user.username

    @staticmethod
    def test_nav_panel_links(visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(ENDPOINT)

        panel = res.soup.select('nav.panel')[-1]
        links = [link['href'] for link in panel.find_all('a', href=True)]

        assert links == [
            url_for('mgnt.view_prompt'),
            url_for('mgnt.view_mapper'),
            url_for('mgnt.view_sensor'),
            url_for('api.prompt.listing'),
            url_for('api.mapper.listing'),
            url_for('api.sensor.listing'),
            url_for('api.owners.listing'),
        ]

    @staticmethod
    def test_user_data_basic(visitor, gen_user_loggedin):
        user = gen_user_loggedin()
        res = visitor(ENDPOINT)
        text = res.soup.text

        assert user.username in text
        assert ICON['bool_right'] in str(res.soup)
        assert user.created_fmt in text
        assert user.last_login_fmt in text

    @staticmethod
    def test_user_data_point(visitor, gen_sensor, gen_user_loggedin):
        user = gen_user_loggedin()
        sensor = gen_sensor()
        amount = 23
        point = [
            Point.create(sensor=sensor, user=user, value=num)
            for num in range(amount)
        ][-1]

        res = visitor(ENDPOINT)
        text = res.soup.text
        assert str(amount) in text
        assert point.created_fmt in text
