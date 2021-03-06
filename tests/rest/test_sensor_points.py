from datetime import datetime, timedelta

from flask import url_for
from flask_restful import marshal
from flask_restful.fields import DateTime, Float, Integer, Nested, String
from pytest import mark

from observatory.models.point import Point
from observatory.rest.sensor import SensorPoints

ENDPOINT = 'api.sensor.points'


@mark.usefixtures('session')
class TestSensorPoints:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT, slug='test') == '/api/sensor/test/points'

    @staticmethod
    def test_get_marshal():
        mdef = SensorPoints.SINGLE_GET
        assert isinstance(mdef['length'], Integer)
        points = mdef['points']
        assert isinstance(points, Nested)
        assert points.default == []
        pnst = points.nested
        assert isinstance(pnst['sensor'], String)
        assert isinstance(pnst['user'], String)
        assert isinstance(pnst['value'], Float)
        stamp = pnst['stamp']
        assert isinstance(stamp, DateTime)
        assert stamp.dt_format == 'iso8601'
        assert stamp.attribute == 'created'

    @staticmethod
    def test_get_empty(visitor):
        res = visitor(ENDPOINT, params={'slug': 'wrong'}, code=404)
        assert 'not present' in res.json['message'].lower()

    @staticmethod
    def test_no_point(visitor, gen_sensor):
        sensor = gen_sensor()
        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorPoints.SINGLE_GET)
        assert res.json['points'] == []

    @staticmethod
    def test_get_with_point(visitor, gen_sensor, gen_user):
        sensor, user = gen_sensor(), gen_user()
        point = Point.create(sensor=sensor, user=user, value=23.42)

        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorPoints.SINGLE_GET)
        assert res.json['points'] == [
            dict(
                sensor=sensor.slug,
                stamp=point.created.isoformat(),
                user=user.username,
                value=point.value,
            )
        ]

    @staticmethod
    def test_points(visitor, gen_sensor, gen_user):
        now = datetime.utcnow()
        sensor, user = gen_sensor(), gen_user()

        old = Point.create(
            sensor=sensor,
            user=user,
            value=0,
            created=(now - timedelta(days=1)),
        )
        new = Point.create(
            sensor=sensor,
            user=user,
            value=1,
            created=(now + timedelta(days=1)),
        )
        assert sensor.points == [new, old]

        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json['points'] == [
            dict(
                sensor=sensor.slug,
                stamp=new.created.isoformat(),
                user=user.username,
                value=new.value,
            ),
            dict(
                sensor=sensor.slug,
                stamp=old.created.isoformat(),
                user=user.username,
                value=old.value,
            ),
        ]
