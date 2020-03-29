from datetime import datetime

from pytest import mark

from stats.models.point import Point
from stats.models.sensor import Sensor
from stats.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestPoint:

    @staticmethod
    def test_default_fields(gen_sensor):
        value = 23.5
        start = datetime.utcnow()
        sensor = gen_sensor()

        point = Point.create(sensor=sensor, value=value)

        assert point.sensor == sensor
        assert point.value == value
        assert start <= point.created
        assert point.created <= datetime.utcnow()

        assert point.created_epoch > 0
        assert point.created_epoch_ms > 0
        assert point.outdated is False

    @staticmethod
    def test_epochs(gen_sensor):
        point = Point.create(sensor=gen_sensor(), value=0)

        assert point.created_epoch <= (
            point.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert point.created_epoch_ms == 1000 * point.created_epoch

    @staticmethod
    def test_created_fmt(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=42)
        assert point.created_fmt == point.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_delete_cascade(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=23.5)

        assert Sensor.query.all() == [sensor]
        assert sensor.points == [point]
        assert Point.query.all() == [point]

        assert point.delete()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []
        assert Point.query.all() == []

    @staticmethod
    def test_outdated(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        olds, news, _ = gen_points_batch(sensor, old=1, new=1)

        assert olds[-1].outdated is True
        assert news[-1].outdated is False

    @staticmethod
    def test_query_outdated(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        olds, _, complete = gen_points_batch(sensor)

        assert Point.query.all() == complete
        assert Point.query_outdated().all() == olds
