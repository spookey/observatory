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
        assert start <= point.stamp
        assert point.stamp <= datetime.utcnow()

        assert point.epoch > 0
        assert point.epoch_ms > 0
        assert point.outdated is False

    @staticmethod
    def test_epochs(gen_sensor):
        point = Point.create(sensor=gen_sensor(), value=0)

        assert point.epoch <= (
            point.stamp - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert point.epoch_ms == 1000 * point.epoch

    @staticmethod
    def test_stamp_fmt(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=42)
        assert point.stamp_fmt == point.stamp.strftime(FMT_STRFTIME)

    @staticmethod
    def test_delete_cascade(gen_sensor):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, value=23.5)

        assert Sensor.query.all() == [sensor]
        assert sensor.points == [point]
        assert Point.query.all() == [point]

        point.delete()

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
