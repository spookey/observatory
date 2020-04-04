from flask import url_for
from flask_restful import marshal
from flask_restful.fields import DateTime, Float, Nested, String, Url
from pytest import mark

from observatory.models.point import Point
from observatory.rest.sensor import SensorSingle

ENDPOINT = 'api.sensor.single'


@mark.usefixtures('session')
class TestSensorSingle:

    @staticmethod
    def test_point_marshal():
        mdef = SensorSingle.SINGLE_GET
        assert isinstance(mdef['points'], Nested)
        nest = mdef['points'].nested
        assert isinstance(nest['value'], Float)
        stamp = nest['stamp']
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
            method='post', code=400,
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
                ENDPOINT, params={'slug': sensor.slug},
                method='post', data=data, code=400,
            )
            assert expect in res.json['message']['value'].lower()

    @staticmethod
    def test_post_no_point(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        setattr(sensor, 'append', lambda _: False)  # crazy monkeypatch
        res = visitor(
            ENDPOINT, params={'slug': sensor.slug},
            method='post', data={'value': 23}, code=500,
        )
        assert 'could not add' in res.json['message'].lower()

    @staticmethod
    @mark.parametrize('_value', [23.42, -1337, 0, float('inf')])
    def test_post_single(_value, visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        sensor = gen_sensor()
        assert Point.query.all() == []

        res = visitor(
            ENDPOINT, params={'slug': sensor.slug},
            method='post', data={'value': _value}, code=201,
        )

        point = Point.query.first()
        assert point.value == _value

        assert res.json == marshal(sensor, SensorSingle.SINGLE_POST)
        assert res.json['value'] == _value
        assert res.json['url'] == url_for(
            'api.sensor.single', slug=sensor.slug, _external=True
        )
