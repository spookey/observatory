from flask import url_for
from flask_restful import marshal
from pytest import mark

from stats.rest.sensor import SensorListing

ENDPOINT = 'api.sensor.listing'


@mark.usefixtures('session')
class TestSensorListing:

    @staticmethod
    def test_url():
        assert url_for(ENDPOINT) == '/api/sensor'

    @staticmethod
    def test_get_empty_listing(visitor):
        res = visitor(ENDPOINT)
        assert res.json == []

    @staticmethod
    def test_get_listing(visitor, gen_sensor):
        sensors = [
            gen_sensor(name='one'), gen_sensor(name='two'),
        ]
        res = visitor(ENDPOINT)
        assert res.json == marshal(sensors, SensorListing.LISTING_GET)
