from pytest import mark

from observatory.models.point import Point
from observatory.models.sensor import Sensor


def _pointsort(points):
    return list(sorted(points, key=lambda p: p.created, reverse=True))


@mark.usefixtures('session')
class TestSensor:
    @staticmethod
    def test_points_field_and_query(gen_sensor):
        sensor = gen_sensor(slug='test')

        assert sensor.points == []
        assert sensor.query_points.all() == []
        assert sensor.query_points.count() == 0
        assert sensor.query_points.first() is None

    @staticmethod
    def test_points_ordered(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, points = gen_points_batch(sensor)

        assert sensor.points == _pointsort(points)
        assert sensor.query_points.all() == _pointsort(points)

    @staticmethod
    def test_delete_cascade_orphan(gen_sensor):
        sensor = gen_sensor()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []

        points = [
            Point.create(sensor=sensor, value=23),
            Point.create(sensor=sensor, value=42),
        ]

        assert Point.query.all() == points
        assert sensor.points == _pointsort(points)

        assert sensor.delete()

        assert Sensor.query.all() == []
        assert Point.query.all() == []

    @staticmethod
    def test_delete_cascade_keep_others(gen_sensor):
        keep_sensor = gen_sensor('keep')
        drop_sensor = gen_sensor('drop')

        assert Sensor.query.all() == [keep_sensor, drop_sensor]
        assert keep_sensor.points == []
        assert drop_sensor.points == []

        keep_point = Point.create(sensor=keep_sensor, value=23)
        drop_point = Point.create(sensor=drop_sensor, value=42)

        assert Point.query.all() == [keep_point, drop_point]

        assert drop_sensor.points == [drop_point]
        assert keep_sensor.points == [keep_point]

        assert drop_sensor.delete()

        assert Sensor.query.all() == [keep_sensor]
        assert Point.query.all() == [keep_point]

    @staticmethod
    def test_length(gen_sensor):
        sensor = gen_sensor()
        assert sensor.length == 0

        points = []
        for num in range(1, 5):
            points.append(Point.create(sensor=sensor, value=num))
            assert sensor.length == num
            assert sensor.points == _pointsort(points)

        assert all(point.delete() for point in points)
        assert sensor.length == 0

    @staticmethod
    def test_latest_empty(gen_sensor):
        sensor = gen_sensor()

        assert sensor.points == []
        assert sensor.query_points.all() == []
        assert sensor.latest is None

    @staticmethod
    def test_latest(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        assert sensor.query_points.all() == _pointsort(complete)
        assert sensor.latest == _pointsort(complete)[0]

    @staticmethod
    def test_cleanup(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        assert sensor.cleanup()

        assert sensor.points == []

    @staticmethod
    def test_cleanup_deletes_all(gen_sensor, gen_points_batch):
        one = gen_sensor('one')
        two = gen_sensor('two')
        _, _, old_one = gen_points_batch(one, old=5, new=0)
        _, _, old_two = gen_points_batch(two, old=5, new=0)

        assert one.points == _pointsort(old_one)
        assert two.points == _pointsort(old_two)
        assert one.cleanup()

        assert one.points == []
        assert two.points == []

    @staticmethod
    def test_append(gen_sensor):
        sensor = gen_sensor()
        assert Point.query.count() == 0
        point = sensor.append(value=42)
        assert Point.query.count() == 1
        assert Point.query.all() == sensor.points
        assert Point.query.first() == point

    @staticmethod
    def test_append_cleanup(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        point = sensor.append(value=23)

        assert point.sensor == sensor
        assert sensor.points == [point]
