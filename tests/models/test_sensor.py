from pytest import mark

from observatory.models.point import Point
from observatory.models.sensor import Sensor
from observatory.models.value import Value


def _pointsort(points):
    return list(sorted(points, key=lambda p: p.created, reverse=True))


@mark.usefixtures('session')
class TestSensor:
    @staticmethod
    def test_fields_and_points_query(gen_sensor):
        sensor = gen_sensor(slug='test')

        assert sensor.points == []
        assert sensor.query_points.all() == []
        assert sensor.query_points.count() == 0
        assert sensor.query_points.first() is None

        assert sensor.values == []

    @staticmethod
    def test_points_ordered(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, points = gen_points_batch(sensor=sensor)

        assert sensor.points == _pointsort(points)
        assert sensor.query_points.all() == _pointsort(points)

    @staticmethod
    def test_values_ordered(gen_sensor):
        sensor = gen_sensor()

        two = Value.create(key='two', idx=2, sensor=sensor)
        one = Value.create(key='one', idx=1, sensor=sensor)
        nil = Value.create(key='nil', idx=0, sensor=sensor)

        assert sensor.values == [nil, one, two]

    @staticmethod
    def test_delete_cascade_orphan_point(gen_sensor, gen_user):
        sensor = gen_sensor()
        user = gen_user()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []

        points = [
            Point.create(sensor=sensor, user=user, value=23),
            Point.create(sensor=sensor, user=user, value=42),
        ]

        assert Point.query.all() == points
        assert sensor.points == _pointsort(points)

        assert sensor.delete()

        assert Sensor.query.all() == []
        assert Point.query.all() == []

    @staticmethod
    def test_delete_cascade_orphan_value(gen_sensor):
        sensor = gen_sensor()

        assert Sensor.query.all() == [sensor]
        assert sensor.values == []

        values = [
            Value.create(sensor=sensor, key='value', idx=0),
            Value.create(sensor=sensor, key='value', idx=1),
        ]

        assert Value.query.all() == values
        assert sensor.values == values

        assert sensor.delete()

        assert Sensor.query.all() == []
        assert Value.query.all() == []

    @staticmethod
    def test_delete_cascade_keep_other_points(gen_sensor, gen_user):
        keep_sensor = gen_sensor('keep')
        drop_sensor = gen_sensor('drop')
        user = gen_user()

        assert Sensor.query.all() == [keep_sensor, drop_sensor]
        assert keep_sensor.points == []
        assert drop_sensor.points == []

        keep_point = Point.create(sensor=keep_sensor, user=user, value=23)
        drop_point = Point.create(sensor=drop_sensor, user=user, value=42)

        assert Point.query.all() == [keep_point, drop_point]

        assert drop_sensor.points == [drop_point]
        assert keep_sensor.points == [keep_point]

        assert drop_sensor.delete()

        assert Sensor.query.all() == [keep_sensor]
        assert Point.query.all() == [keep_point]

    @staticmethod
    def test_delete_cascade_keep_other_values(gen_sensor):
        keep_sensor = gen_sensor('keep')
        drop_sensor = gen_sensor('drop')

        assert Sensor.query.all() == [keep_sensor, drop_sensor]
        assert keep_sensor.values == []
        assert drop_sensor.values == []

        keep_value = Value.create(sensor=keep_sensor, key='value', idx=1)
        drop_value = Value.create(sensor=drop_sensor, key='value', idx=0)

        assert Value.query.all() == [keep_value, drop_value]

        assert drop_sensor.delete()

        assert Sensor.query.all() == [keep_sensor]
        assert Value.query.all() == [keep_value]

    @staticmethod
    def test_length(gen_sensor, gen_user):
        sensor = gen_sensor()
        user = gen_user()
        assert sensor.length == 0

        points = []
        for num in range(1, 5):
            points.append(Point.create(sensor=sensor, user=user, value=num))
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
        _, _, complete = gen_points_batch(sensor=sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        assert sensor.query_points.all() == _pointsort(complete)
        assert sensor.latest == _pointsort(complete)[0]

    @staticmethod
    def test_cleanup(gen_sensor, gen_points_batch):
        sensor = gen_sensor()
        _, _, complete = gen_points_batch(sensor=sensor, old=5, new=0)

        assert sensor.points == _pointsort(complete)
        assert sensor.cleanup()

        assert sensor.points == []

    @staticmethod
    def test_cleanup_deletes_all(gen_sensor, gen_user, gen_points_batch):
        one = gen_sensor('one')
        two = gen_sensor('two')
        user = gen_user()
        _, _, old_one = gen_points_batch(sensor=one, user=user, old=5, new=0)
        _, _, old_two = gen_points_batch(sensor=two, user=user, old=5, new=0)

        assert one.points == _pointsort(old_one)
        assert two.points == _pointsort(old_two)
        assert one.cleanup()

        assert one.points == []
        assert two.points == []

    @staticmethod
    def test_append(gen_sensor, gen_user):
        sensor = gen_sensor()
        assert Point.query.count() == 0
        point = sensor.append(user=gen_user(), value=42)
        assert Point.query.count() == 1
        assert Point.query.all() == sensor.points
        assert Point.query.first() == point

    @staticmethod
    def test_append_cleanup(gen_sensor, gen_user, gen_points_batch):
        sensor = gen_sensor()
        user = gen_user()
        _, _, complete = gen_points_batch(
            sensor=sensor, user=user, old=5, new=0
        )

        assert sensor.points == _pointsort(complete)
        point = sensor.append(user=user, value=23)

        assert point.sensor == sensor
        assert point.user == user
        assert sensor.points == [point]
