from stats.models.user import User
from pytest import mark
from pytest import fixture


@fixture(scope='function')
def invoke(ctx_app):
    runner = ctx_app.test_cli_runner()

    def run(*args):
        elems = ['cli']
        elems.extend(args)
        return runner.invoke(args=elems)
    return run

# pylint: disable=redefined-outer-name


@mark.usefixtures('session')
class TestCli:

    @staticmethod
    def test_adduser(invoke):
        username = 'user'
        password = 'pass'
        assert User.query.all() == []

        result = invoke(
            'adduser', '--username', username, '--password', password
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
            'adduser', '--username', user.username, '--password', 'pass'
        )
        assert 'already present' in result.output.lower()

        assert User.query.all() == [user]

    @staticmethod
    def test_setpass(invoke, gen_user):
        pass_old = '_old'
        pass_new = '_new'

        user = gen_user(password=pass_old)
        assert user.check_password(pass_old) is True
        assert user.check_password(pass_new) is False

        result = invoke(
            'setpass', '--username', user.username, '--password', pass_new
        )
        assert 'password changed' in result.output.lower()

        user = User.query.first()
        assert user.check_password(pass_old) is False
        assert user.check_password(pass_new) is True

    @staticmethod
    def test_setpass_not_found(invoke):
        assert User.query.all() == []

        result = invoke(
            'setpass', '--username', 'user', '--password', 'pass'
        )
        assert 'not found' in result.output.lower()

    @staticmethod
    def test_setstate(invoke, gen_user):
        user = gen_user()
        assert user.active is True

        result = invoke(
            'setstate', '--username', user.username, '--blocked'
        )
        assert 'changed to blocked' in result.output.lower()

        user = User.query.first()
        assert user.active is False

        result = invoke(
            'setstate', '--username', user.username, '--active'
        )
        assert 'changed to active' in result.output.lower()

        user = User.query.first()
        assert user.active is True

    @staticmethod
    def test_setstate_not_found(invoke):
        assert User.query.all() == []

        result = invoke(
            'setstate', '--username', 'user', '--blocked'
        )
        assert 'not found' in result.output.lower()
