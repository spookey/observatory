from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from observatory.models.point import Point
from observatory.models.user import User
from observatory.start.environment import FMT_STRFTIME


def _pointsort(points):
    return list(sorted(points, key=lambda p: p.created, reverse=True))


@mark.usefixtures('session')
class TestUser:
    @staticmethod
    def test_default_fields(gen_user):
        start = datetime.utcnow()

        username = 'user'
        password = 'very-secure-23'

        user = gen_user(username=username, password=password)

        assert user.username == username
        assert user.active is True
        assert user.last_login is None

        assert start <= user.created
        assert user.created <= datetime.utcnow()

        assert user.points == []
        assert user.query_points.all() == []
        assert user.query_points.count() == 0
        assert user.query_points.first() is None

    @staticmethod
    def test_name_unique(gen_user):
        name = 'user'

        one = gen_user(username=name, _commit=False)
        assert one.save(_commit=True)

        two = gen_user(username=name, _commit=False)

        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_by_username(gen_user):
        one = gen_user(username='one')
        two = gen_user(username='two')

        assert User.query.all() == [one, two]

        assert User.by_username('one') == one
        assert User.by_username('two') == two

    @staticmethod
    def test_get_id(gen_user):
        one = gen_user(username='one')
        two = gen_user(username='two')

        assert one.get_id() == f'{one.prime}'
        assert two.get_id() == f'{two.prime}'

    @staticmethod
    def test_is_active(gen_user):
        user = gen_user()

        assert user.active is True
        assert user.is_active == user.active

        user.active = False
        assert user.save()

        assert user.active is False
        assert user.is_active == user.active

    @staticmethod
    def test_created_fmt(gen_user):
        user = gen_user()
        assert user.created_fmt == user.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_created_epoch(gen_user):
        user = gen_user()
        assert (
            user.created_epoch
            <= (user.created - datetime.utcfromtimestamp(0)).total_seconds()
        )
        assert user.created_epoch_ms == 1000 * user.created_epoch

    @staticmethod
    def test_hash_password():
        assert User.hash_password(None) is None
        pw_text = 'secret'
        pw_hash = User.hash_password(pw_text)

        assert pw_hash != pw_text
        assert isinstance(pw_hash, bytes)
        assert pw_hash != pw_text.encode()

        assert pw_hash.startswith(b'$2b$')

    @staticmethod
    def test_null_password(gen_user):
        user = gen_user(password=None)
        assert user.pw_hash is None
        assert user.check_password(None) is False

        assert user.set_password(None, _commit=True)

        assert user.pw_hash is None
        assert user.check_password(None) is False

    @staticmethod
    def test_set_check_password(gen_user):
        pw1 = 'secure'
        pw2 = 'secret'
        user = gen_user(password=pw1)

        assert user.pw_hash != pw1
        assert user.pw_hash != pw2
        assert user.check_password(pw1) is True
        assert user.check_password(pw2) is False

        assert user.set_password(pw2, _commit=True)

        assert user.pw_hash != pw1
        assert user.pw_hash != pw2
        assert user.check_password(pw1) is False
        assert user.check_password(pw2) is True

    @staticmethod
    def test_refresh(gen_user):
        start = datetime.utcnow()
        user = gen_user()

        assert user.last_login is None

        refreshed = user.refresh()
        assert refreshed == user

        assert start <= user.last_login
        assert user.last_login <= datetime.utcnow()

    @staticmethod
    def test_last_login_fmt(gen_user):
        user = gen_user()
        assert user.last_login_fmt == ''

        assert user.refresh()

        assert user.last_login_fmt == user.last_login.strftime(FMT_STRFTIME)

    @staticmethod
    def test_last_login_epoch(gen_user):
        user = gen_user()
        assert user.last_login_epoch is None
        assert user.last_login_epoch_ms is None

        assert user.refresh()

        assert (
            user.last_login_epoch
            <= (user.last_login - datetime.utcfromtimestamp(0)).total_seconds()
        )
        assert user.last_login_epoch_ms == 1000 * user.last_login_epoch

    @staticmethod
    def test_points_ordered(gen_user, gen_points_batch):
        user = gen_user()
        _, _, points = gen_points_batch(user=user)

        assert user.points == _pointsort(points)
        assert user.query_points.all() == _pointsort(points)

    @staticmethod
    def test_delete_cascade_orphan(gen_user, gen_sensor):
        sensor = gen_sensor()
        user = gen_user()

        assert User.query.all() == [user]
        assert user.points == []

        points = [
            Point.create(sensor=sensor, user=user, value=23),
            Point.create(sensor=sensor, user=user, value=42),
        ]

        assert Point.query.all() == points
        assert user.points == _pointsort(points)

        assert user.delete()

        assert User.query.all() == []
        assert Point.query.all() == []

    @staticmethod
    def test_delete_cascade_keep_others(gen_sensor, gen_user):
        sensor = gen_sensor()
        keep_user = gen_user('keep')
        drop_user = gen_user('drop')

        assert User.query.all() == [keep_user, drop_user]
        assert keep_user.points == []
        assert drop_user.points == []

        keep_point = Point.create(sensor=sensor, user=keep_user, value=23)
        drop_point = Point.create(sensor=sensor, user=drop_user, value=42)

        assert Point.query.all() == [keep_point, drop_point]

        assert drop_user.points == [drop_point]
        assert keep_user.points == [keep_point]

        assert drop_user.delete()

        assert User.query.all() == [keep_user]
        assert Point.query.all() == [keep_point]

    @staticmethod
    def test_length(gen_sensor, gen_user):
        sensor = gen_sensor()
        user = gen_user()
        assert user.length == 0

        points = []
        for num in range(1, 5):
            points.append(Point.create(sensor=sensor, user=user, value=num))
            assert user.length == num
            assert user.points == _pointsort(points)

        assert all(point.delete() for point in points)
        assert user.length == 0

    @staticmethod
    def test_latest_empty(gen_user):
        user = gen_user()

        assert user.points == []
        assert user.query_points.all() == []
        assert user.latest is None

    @staticmethod
    def test_latest(gen_user, gen_points_batch):
        user = gen_user()
        _, _, complete = gen_points_batch(user=user, old=5, new=0)

        assert user.points == _pointsort(complete)
        assert user.query_points.all() == _pointsort(complete)
        assert user.latest == _pointsort(complete)[0]
