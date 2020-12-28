from datetime import datetime, timedelta

from flask import url_for
from flask_restful import marshal
from flask_restful.fields import DateTime, Float, Integer, Nested, String, Url
from pytest import mark

from observatory.models.point import Point
from observatory.rest.sensor import SensorSingle

ENDPOINT = 'api.sensor.single'


@mark.usefixtures('session')
class TestSensorSingle:
    @staticmethod
    def test_get_marshal():
        mdef = SensorSingle.SINGLE_GET
        assert isinstance(mdef['length'], Integer)
        latest = mdef['latest']
        assert isinstance(latest, Nested)
        assert latest.default == {}
        lnst = latest.nested
        assert isinstance(lnst['value'], Float)
        stamp = lnst['stamp']
        assert isinstance(stamp, DateTime)
        assert stamp.dt_format == 'iso8601'
        assert stamp.attribute == 'created'

    @staticmethod
    def test_post_marshal():
        mdef = SensorSingle.SINGLE_POST
        assert isinstance(mdef['slug'], String)
        assert isinstance(mdef['value'], Float)
        url = mdef['url']
        assert isinstance(url, Url)
        assert url.absolute is True
        assert url.endpoint == 'api.sensor.single'

    @staticmethod
    def test_no_point(visitor, gen_sensor):
        sensor = gen_sensor()
        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorSingle.SINGLE_GET)
        assert res.json['latest'] == {}

    @staticmethod
    def test_get_with_point(visitor, gen_sensor, gen_user):
        sensor, user = gen_sensor(), gen_user()
        point = Point.create(sensor=sensor, user=user, value=23.42)

        res = visitor(ENDPOINT, params={'slug': sensor.slug})
        assert res.json == marshal(sensor, SensorSingle.SINGLE_GET)
        assert res.json['latest']['value'] == point.value

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

        res = visitor(ENDPOINT, params={'slug': sensor.slug}, code=200)
        assert res.json['latest']['stamp'] == new.created.isoformat()
        assert res.json['latest']['value'] == new.value

    @staticmethod
    def test_post_not_logged_in(visitor, gen_sensor):
        sensor = gen_sensor()
        visitor(
            ENDPOINT, params={'slug': sensor.slug}, method='post', code=401
        )

    @staticmethod
    def test_post_empty(visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(
            ENDPOINT,
            params={'slug': 'test'},
            method='post',
            code=400,
        )
        assert res.json.get('message', None) is not None

    @staticmethod
    def test_post_wrong(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        for data, expect in (
            ({'some': 'thing'}, 'missing required parameter'),
            ({'value': None}, 'missing required parameter'),
            ({'value': 'error'}, 'could not convert string to float'),
        ):
            res = visitor(
                ENDPOINT,
                params={'slug': sensor.slug},
                method='post',
                data=data,
                code=400,
            )
            assert expect in res.json['message']['value'].lower()

    @staticmethod
    def test_post_no_point(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        setattr(sensor, 'append', lambda *_, **__: False)  # crazy monkeypatch

        res = visitor(
            ENDPOINT,
            params={'slug': sensor.slug},
            method='post',
            data={'value': 23},
            code=500,
        )
        assert 'could not add' in res.json['message'].lower()

    @staticmethod
    @mark.parametrize('value', [23.42, -1337, 0, float('inf')])
    def test_post_single(value, visitor, gen_sensor, gen_user_loggedin):
        user = gen_user_loggedin()
        sensor = gen_sensor()
        assert Point.query.all() == []

        res = visitor(
            ENDPOINT,
            params={'slug': sensor.slug},
            method='post',
            data={'value': value},
            code=201,
        )

        point = Point.query.first()
        assert point.value == value
        assert point.user == user

        assert res.json == marshal(sensor, SensorSingle.SINGLE_POST)
        assert res.json['value'] == value
        assert res.json['url'] == url_for(
            'api.sensor.single', slug=sensor.slug, _external=True
        )
