from datetime import datetime, timedelta

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
from observatory.rest.owners import OwnersSingle

ENDPOINT = 'api.owners.single'


@mark.usefixtures('session')
class TestOwnersSingle:
    @staticmethod
    def test_marshal():
        mdef = OwnersSingle.SINGLE_GET
        assert isinstance(mdef['name'], String)
        assert isinstance(mdef['active'], Boolean)
        assert isinstance(mdef['created'], DateTime)
        assert isinstance(mdef['last_login'], DateTime)
        assert isinstance(mdef['length'], Integer)
        latest = mdef['latest']
        assert isinstance(latest, Nested)
        assert latest.default == {}
        lnst = latest.nested
        assert isinstance(lnst['sensor'], String)
        assert isinstance(lnst['user'], String)
        assert isinstance(lnst['value'], Float)
        stamp = lnst['stamp']
        assert isinstance(stamp, DateTime)
        assert stamp.dt_format == 'iso8601'
        assert stamp.attribute == 'created'

    @staticmethod
    def test_no_point(visitor, gen_user):
        user = gen_user()
        res = visitor(ENDPOINT, params={'username': user.username})
        assert res.json == marshal(user, OwnersSingle.SINGLE_GET)
        assert res.json['latest'] == {}

    @staticmethod
    def test_with_point(visitor, gen_sensor, gen_user):
        sensor, user = gen_sensor(), gen_user()
        point = Point.create(sensor=sensor, user=user, value=23.42)

        res = visitor(ENDPOINT, params={'username': user.username})
        assert res.json == marshal(user, OwnersSingle.SINGLE_GET)
        assert res.json['latest'] == dict(
            sensor=sensor.slug,
            stamp=point.created.isoformat(),
            user=user.username,
            value=point.value,
        )

    @staticmethod
    def test_latest(visitor, gen_sensor, gen_user):
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
        assert sensor.latest == new

        res = visitor(ENDPOINT, params={'username': user.username})
        assert res.json['latest'] == dict(
            sensor=sensor.slug,
            stamp=new.created.isoformat(),
            user=user.username,
            value=new.value,
        )
