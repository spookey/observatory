from datetime import datetime, timedelta

from flask import url_for
from flask_restful import marshal
from flask_restful.fields import (
    Boolean,
    DateTime,
    Float,
    Integer,
    Nested,
    String,
)
from pytest import mark

from observatory.models.point import Point
from observatory.rest.owners import OwnersPoints

ENDPOINT = 'api.owners.points'


@mark.usefixtures('session')
class TestOwnersPoints:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT, username='test') == '/api/user/test/points'

    @staticmethod
    def test_marshal():
        mdef = OwnersPoints.SINGLE_GET
        assert isinstance(mdef['name'], String)
        assert isinstance(mdef['active'], Boolean)
        assert isinstance(mdef['created'], DateTime)
        assert isinstance(mdef['last_login'], DateTime)
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
        res = visitor(ENDPOINT, params={'username': 'wrong'}, code=404)
        assert 'not present' in res.json['message'].lower()

    @staticmethod
    def test_no_point(visitor, gen_user):
        user = gen_user()
        res = visitor(ENDPOINT, params={'username': user.username})
        assert res.json == marshal(user, OwnersPoints.SINGLE_GET)
        assert res.json['points'] == []

    @staticmethod
    def test_with_point(visitor, gen_sensor, gen_user):
        sensor, user = gen_sensor(), gen_user()
        point = Point.create(sensor=sensor, user=user, value=23.42)

        res = visitor(ENDPOINT, params={'username': user.username})
        assert res.json == marshal(user, OwnersPoints.SINGLE_GET)
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

        res = visitor(ENDPOINT, params={'username': user.username})
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
