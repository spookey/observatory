from datetime import datetime, timedelta

from flask import url_for
from flask_restful.fields import DateTime, Float, String
from pytest import mark

from observatory.models.point import Point
from observatory.rest.generic import SlugUrl
from observatory.rest.sensor import SensorLatest

ENDPOINT = 'api.sensor.latest'


@mark.usefixtures('session')
class TestSensorLatest:

    @staticmethod
    def test_url():
        assert url_for(ENDPOINT, slug='test') == '/api/sensor/test/latest'

    @staticmethod
    def test_marshal():
        mdef = SensorLatest.SINGLE_GET
        slug = mdef['slug']
        assert isinstance(slug, String)
        assert slug.attribute == 'sensor.slug'
        stamp = mdef['stamp']
        assert isinstance(stamp, DateTime)
        assert stamp.attribute == 'created'
        assert stamp.dt_format == 'iso8601'
        url = mdef['url']
        assert isinstance(url, SlugUrl)
        assert url.absolute is True
        assert url.attribute == 'sensor'
        assert url.endpoint == 'api.sensor.single'
        assert isinstance(mdef['value'], Float)

    @staticmethod
    def test_sensor_empty(visitor):
        res = visitor(ENDPOINT, params={'slug': 'wrong'}, code=404)
        assert 'not present' in res.json['message'].lower()

    @staticmethod
    def test_latest_empty(visitor, gen_sensor):
        sensor = gen_sensor()
        res = visitor(ENDPOINT, params={'slug': sensor.slug}, code=500)
        assert 'no values' in res.json['message'].lower()

    @staticmethod
    def test_latest(visitor, gen_sensor):
        now = datetime.utcnow()
        sensor = gen_sensor()

        old = Point.create(
            sensor=sensor, value=0, created=(now - timedelta(days=1))
        )
        new = Point.create(
            sensor=sensor, value=1, created=(now + timedelta(days=1))
        )
        assert sensor.points == [new, old]
        assert sensor.latest == new

        res = visitor(ENDPOINT, params={'slug': sensor.slug}, code=200)
        assert res.json['slug'] == sensor.slug
        assert res.json['stamp'] == new.created.isoformat()
        assert res.json['url'] == url_for(
            'api.sensor.single',
            slug=sensor.slug,
            _external=True
        )
        assert res.json['value'] == new.value
