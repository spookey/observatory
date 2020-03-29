from pytest import mark

from stats.models.point import Point
from stats.models.sensor import Sensor


def _pointsort(points):
    return list(sorted(
        points, key=lambda p: p.created, reverse=True
    ))


@mark.usefixtures('session')
class TestSensor:

    @staticmethod
    def test_points_field(gen_sensor):
        sensor = gen_sensor(slug='test')

        assert sensor.points == []

    @staticmethod
    def test_delete_cascade(gen_sensor):
        sensor = gen_sensor()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []

        point = Point.create(sensor=sensor, value=42)

        assert Point.query.all() == [point]
        assert sensor.points == [point]

        assert sensor.delete()

        assert Sensor.query.all() == []
        assert Point.query.all() == []

    @staticmethod
    def test_backref_ordered(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, points = gen_points_batch(sensor)

        assert sensor.points == _pointsort(points)

    @staticmethod
    def test_query_points_outdated(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        olds, _, complete = gen_points_batch(sensor)

        assert sensor.points == _pointsort(complete)
        assert sensor.query_points_outdated().all() == _pointsort(olds)

    @staticmethod
    def test_cleanup(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        sensor.cleanup()

        assert sensor.points == []

    @staticmethod
    def test_append(gen_sensor):
        sensor = gen_sensor()
        assert Point.query.count() == 0
        sensor.append(42)
        assert Point.query.count() == 1
        assert Point.query.all() == sensor.points

    @staticmethod
    def test_append_cleanup(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        point = sensor.append(value=23)

        assert point.sensor == sensor
        assert sensor.points == [point]
