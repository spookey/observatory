from datetime import datetime

from pytest import mark

from observatory.models.mapper import EnumConvert, EnumHorizon
from observatory.models.point import Point
from observatory.models.sensor import Sensor
from observatory.models.user import User
from observatory.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestPoint:
    @staticmethod
    def test_default_fields(gen_sensor, gen_user):
        value = 23.5
        start = datetime.utcnow()
        sensor = gen_sensor()
        user = gen_user()

        point = Point.create(sensor=sensor, user=user, value=value)

        assert point.sensor == sensor
        assert point.user == user
        assert point.value == value

        assert start <= point.created
        assert point.created <= datetime.utcnow()
        assert point.created_epoch > 0
        assert point.created_epoch_ms > 0
        assert point.outdated is False

    @staticmethod
    def test_epochs(gen_sensor, gen_user):
        point = Point.create(sensor=gen_sensor(), user=gen_user(), value=0)

        assert (
            point.created_epoch
            <= (point.created - datetime.utcfromtimestamp(0)).total_seconds()
        )
        assert point.created_epoch_ms == 1000 * point.created_epoch

    @staticmethod
    def test_created_fmt(gen_sensor, gen_user):
        point = Point.create(sensor=gen_sensor(), user=gen_user(), value=42)
        assert point.created_fmt == point.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_sensor_delete_cascade(gen_sensor, gen_user):
        sensor = gen_sensor()
        point = Point.create(sensor=sensor, user=gen_user(), value=23.5)

        assert Sensor.query.all() == [sensor]
        assert sensor.points == [point]
        assert Point.query.all() == [point]

        assert point.delete()

        assert Sensor.query.all() == [sensor]
        assert sensor.points == []
        assert Point.query.all() == []

    @staticmethod
    def test_user_delete_cascade(gen_sensor, gen_user):
        user = gen_user()
        point = Point.create(sensor=gen_sensor(), user=user, value=23.5)

        assert User.query.all() == [user]
        assert user.points == [point]
        assert Point.query.all() == [point]

        assert point.delete()

        assert User.query.all() == [user]
        assert user.points == []
        assert Point.query.all() == []

    @staticmethod
    def test_outdated(gen_points_batch):
        olds, news, _ = gen_points_batch(old=1, new=1)

        assert olds[-1].outdated is True
        assert news[-1].outdated is False

    @staticmethod
    def test_query_outdated(gen_points_batch):
        olds, news, complete = gen_points_batch()

        assert Point.query.all() == complete
        assert Point.query_outdated(outdated=True).all() == olds
        assert Point.query_outdated(outdated=False).all() == news

    @staticmethod
    @mark.parametrize(
        ('config', 'nnp'),
        [
            (
                dict(horizon=None, convert=None, elevate=1.0, numeric=False),
                (-23.5, 0.0, 13.37),
            ),
            (
                dict(horizon=None, convert=None, elevate=1.0, numeric=True),
                (-23.5, 0.0, 13.37),
            ),
            (
                dict(horizon=None, convert=None, elevate=0.0, numeric=False),
                (0.0, 0.0, 0.0),
            ),
            (
                dict(horizon=None, convert=None, elevate=0.0, numeric=True),
                (0.0, 0.0, 0.0),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=False,
                ),
                (-23.5, 0.0, 13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=True,
                ),
                (-23.5, 0.0, 13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.NATURAL,
                    elevate=5.0,
                    numeric=False,
                ),
                (-117.5, 0.0, 66.85),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.NATURAL,
                    elevate=5.0,
                    numeric=True,
                ),
                (-117.5, 0.0, 66.85),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=False,
                ),
                (23.5, 0.0, -13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=True,
                ),
                (23.5, 0.0, -13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=False,
                ),
                (23.5, 0.0, -13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=1.0,
                    numeric=True,
                ),
                (23.5, 0.0, -13.37),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=5.0,
                    numeric=False,
                ),
                (117.5, 0.0, -66.85),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.NATURAL,
                    elevate=5.0,
                    numeric=True,
                ),
                (117.5, 0.0, -66.85),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.INTEGER,
                    elevate=1.0,
                    numeric=False,
                ),
                (-24, 0, 13),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.INTEGER,
                    elevate=1.0,
                    numeric=True,
                ),
                (-24, 0, 13),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.INTEGER,
                    elevate=5.0,
                    numeric=False,
                ),
                (-118, 0, 67),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.INTEGER,
                    elevate=5.0,
                    numeric=True,
                ),
                (-118, 0, 67),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.INTEGER,
                    elevate=1.0,
                    numeric=False,
                ),
                (24, 0, -13),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.INTEGER,
                    elevate=1.0,
                    numeric=True,
                ),
                (24, 0, -13),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.INTEGER,
                    elevate=5.0,
                    numeric=False,
                ),
                (118, 0, -67),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.INTEGER,
                    elevate=5.0,
                    numeric=True,
                ),
                (118, 0, -67),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.BOOLEAN,
                    elevate=1.0,
                    numeric=False,
                ),
                (True, False, True),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.BOOLEAN,
                    elevate=1.0,
                    numeric=True,
                ),
                (1.0, 0.0, 1.0),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.BOOLEAN,
                    elevate=5.0,
                    numeric=False,
                ),
                (True, False, True),
            ),
            (
                dict(
                    horizon=EnumHorizon.NORMAL,
                    convert=EnumConvert.BOOLEAN,
                    elevate=5.0,
                    numeric=True,
                ),
                (5.0, 0.0, 5.0),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.BOOLEAN,
                    elevate=1.0,
                    numeric=False,
                ),
                (True, False, True),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.BOOLEAN,
                    elevate=1.0,
                    numeric=True,
                ),
                (-1.0, 0.0, -1.0),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.BOOLEAN,
                    elevate=5.0,
                    numeric=False,
                ),
                (True, False, True),
            ),
            (
                dict(
                    horizon=EnumHorizon.INVERT,
                    convert=EnumConvert.BOOLEAN,
                    elevate=5.0,
                    numeric=True,
                ),
                (-5.0, 0.0, -5.0),
            ),
        ],
    )
    def test_translate(config, nnp, gen_sensor, gen_user):
        sensor = gen_sensor()
        user = gen_user()

        neg = sensor.append(user=user, value=-23.5)
        nil = sensor.append(user=user, value=0)
        pos = sensor.append(user=user, value=13.37)

        for point, expect in zip((neg, nil, pos), nnp):
            assert point.translate(**config) == expect
