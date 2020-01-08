from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from stats.models.point import Point
from stats.models.sensor import Sensor
from stats.start.environment import FMT_STRFTIME


def _pointsort(points):
    return list(sorted(
        points, key=lambda p: p.stamp, reverse=True
    ))


@mark.usefixtures('session')
class TestSensor:

    @staticmethod
    def test_default_fields(gen_sensor):
        start = datetime.utcnow()
        name = 'test'
        title = 'Some test sensor'
        description = 'Description of some test sensor'

        sensor = gen_sensor(name=name, title=title, description=description)

        assert sensor.name == name
        assert sensor.title == title
        assert sensor.description == description

        assert start <= sensor.created
        assert sensor.created <= datetime.utcnow()

        assert sensor.points == []
        assert sensor.displays == []

    @staticmethod
    def test_name_unique(gen_sensor):
        one = gen_sensor(name='demo', title='one', _commit=False)
        assert one.save(_commit=True)

        two = gen_sensor(name='demo', title='two', _commit=False)
        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_by_name(gen_sensor):
        one = gen_sensor(name='one')
        two = gen_sensor(name='two')

        assert Sensor.query.all() == [one, two]

        assert Sensor.by_name('one') == one
        assert Sensor.by_name('two') == two

    @staticmethod
    def test_created_fmt(gen_sensor):
        sensor = gen_sensor()
        assert sensor.created_fmt == sensor.created.strftime(FMT_STRFTIME)

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
