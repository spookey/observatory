from datetime import datetime, timedelta

from pytest import fixture, mark

from observatory.models.point import Point
from observatory.models.sensor import Sensor
from observatory.models.user import User
from observatory.start.environment import BACKLOG_DAYS


@fixture(scope='function')
def invoke(ctx_app):
    runner = ctx_app.test_cli_runner()

    def run(*args):
        return runner.invoke(args=[
            'cli', *(arg for arg in args if arg is not None)
        ])

    yield run

# pylint: disable=redefined-outer-name


@mark.usefixtures('session')
class TestCli:

    @staticmethod
    def test_adduser(invoke):
        username = 'user'
        password = 'pass'
        assert User.query.all() == []

        result = invoke(
            'adduser', '--username', username, '--password', password,
        )
        assert 'created' in result.output.lower()

        user = User.query.first()
        assert user is not None
        assert user.username == username
        assert user.check_password(password) is True

    @staticmethod
    def test_adduser_existing(invoke, gen_user):
        user = gen_user()
        assert User.query.all() == [user]

        result = invoke(
            'adduser', '--username', user.username, '--password', 'pass',
        )
        assert 'already present' in result.output.lower()

        assert User.query.all() == [user]

    @staticmethod
    def test_adduser_invalid_name(invoke):
        assert User.query.all() == []

        result = invoke(
            'adduser', '--username', '🙋‍♀️', '--password', '🤷‍♀️',
        )
        assert 'invalid name' in result.output

        assert User.query.all() == []

    @staticmethod
    def test_setpass(invoke, gen_user):
        pass_old = '_old'
        pass_new = '_new'

        user = gen_user(password=pass_old)
        assert user.check_password(pass_old) is True
        assert user.check_password(pass_new) is False

        result = invoke(
            'setpass', '--username', user.username, '--password', pass_new,
        )
        assert 'password changed' in result.output.lower()

        user = User.query.first()
        assert user.check_password(pass_old) is False
        assert user.check_password(pass_new) is True

    @staticmethod
    def test_setpass_not_found(invoke):
        assert User.query.all() == []

        result = invoke(
            'setpass', '--username', 'user', '--password', 'pass',
        )
        assert 'not found' in result.output.lower()

    @staticmethod
    def test_setstate(invoke, gen_user):
        user = gen_user()
        assert user.active is True

        result = invoke(
            'setstate', '--username', user.username, '--blocked',
        )
        assert 'changed to blocked' in result.output.lower()

        user = User.query.first()
        assert user.active is False

        result = invoke(
            'setstate', '--username', user.username, '--active',
        )
        assert 'changed to active' in result.output.lower()

        user = User.query.first()
        assert user.active is True

    @staticmethod
    def test_setstate_not_found(invoke):
        assert User.query.all() == []

        result = invoke(
            'setstate', '--username', 'user', '--blocked',
        )
        assert 'not found' in result.output.lower()

    @staticmethod
    def test_sensorcurve(invoke, gen_sensor):
        axc = 5
        num = 1 + 2 * axc
        sensor = gen_sensor()
        assert Point.query.count() == 0

        result = invoke(
            'sensorcurve', '--slug', sensor.slug, '--axc', axc,
        )
        assert f'created {num}' in result.output.lower()

        assert Point.query.count() == num

    @staticmethod
    @mark.parametrize('params', [
        (1, '--keep-old',),
        (0, None,),
    ])
    def test_sensorcurve_keep_old(invoke, gen_sensor, params):
        plus, flag = params

        axc = 2
        num = 1 + 2 * axc
        sensor = gen_sensor()
        point = Point.create(
            sensor=sensor, value=42,
            created=datetime.utcnow() - timedelta(days=2 * BACKLOG_DAYS),
        )
        assert Point.query.all() == [point]

        invoke(
            'sensorcurve', '--slug', sensor.slug, '--axc', axc, flag,
        )
        assert Point.query.count() == plus + num

    @staticmethod
    def test_sensorcurve_not_found(invoke):
        assert Sensor.query.all() == []

        result = invoke(
            'sensorcurve', '--slug', 'test',
        )
        assert 'not present' in result.output.lower()

    @staticmethod
    def test_sensorclear(invoke, gen_sensor):
        sensor = gen_sensor()
        number = 23
        for num in range(1, 1 + number):
            sensor.append(num)

        assert Point.query.count() == number

        result = invoke(
            'sensorclear', '--slug', sensor.slug,
        )
        assert f'deleted {number}' in result.output.lower()

        assert Point.query.count() == 0

    @staticmethod
    def test_sensorclear_not_found(invoke):
        assert Sensor.query.all() == []

        result = invoke(
            'sensorclear', '--slug', 'test',
        )
        assert 'not present' in result.output.lower()
