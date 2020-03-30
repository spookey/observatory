from flask_restful import fields, marshal
from pytest import mark

from stats.models.point import Point
from stats.rest.sensor import SensorSingle

ENDPOINT = 'api.sensor.single'


@mark.usefixtures('session')
class TestSensorSingle:

    @staticmethod
    def test_point_marshal():
        points = SensorSingle.SINGLE_GET['points']
        assert isinstance(points, fields.Nested)

        mdef = points.nested
        assert isinstance(mdef['value'], fields.Float)
        stamp = mdef['stamp']
        assert isinstance(stamp, fields.DateTime)
        assert stamp.attribute == 'created'
        assert stamp.dt_format == 'iso8601'

    @staticmethod
    def test_get_with_point(visitor, gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=23.42)

        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorSingle.SINGLE_GET)
        assert res.json['points'][-1]['value'] == point.value

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
