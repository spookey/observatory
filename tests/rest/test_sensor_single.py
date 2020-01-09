from flask import url_for
from flask_restful import marshal
from pytest import mark

from stats.models.point import Point
from stats.rest.sensor import SensorSingle

ENDPOINT = 'api.sensor.single'


@mark.usefixtures('session')
class TestSensorSingle:

    @staticmethod
    def test_url():
        assert url_for(ENDPOINT, slug='test') == '/api/sensor/test'

    @staticmethod
    def test_get_empty_single(visitor):
        res = visitor(ENDPOINT, params={'slug': 'error'}, code=404)
        msg = res.json.get('message', None)
        assert msg
        assert 'not present' in msg.lower()

    @staticmethod
    def test_get_single(visitor, gen_sensor):
        sensor = gen_sensor()
        Point.create(sensor=sensor, value=23.42)

        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorSingle.SINGLE_GET)

    @staticmethod
    def test_post_not_logged_in(visitor, gen_sensor):
        sensor = gen_sensor()
        visitor(
            ENDPOINT, params={'slug': sensor.slug},
            method='post', code=401
        )

    @staticmethod
    def test_post_empty(visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(
            ENDPOINT, params={'slug': 'test'},
            method='post', code=400
        )
        assert res.json.get('message', None) is not None

    @staticmethod
    def test_post_wrong(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        for data in (
                {'some': 'thing'},
                {'value': None},
                {'value': 'error'},
        ):
            visitor(
                ENDPOINT, params={'slug': sensor.slug},
                method='post', data=data, code=400
            )

    @staticmethod
    def test_post_single(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        assert Point.query.all() == []

        value = 23.42
        res = visitor(
            ENDPOINT, params={'slug': sensor.slug},
            method='post', data={'value': value}, code=201
        )

        point = Point.query.first()
        assert point.value == value

        assert res.json == marshal(sensor, SensorSingle.SINGLE_POST)
