from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from observatory.models.user import User
from observatory.start.environment import FMT_STRFTIME


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

    @staticmethod
    def test_name_unique(gen_user):
        one = gen_user(username='user', _commit=False)
        assert one.save(_commit=True)

        two = gen_user(username='user', _commit=False)
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
        assert user.created_epoch <= (
            user.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
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

        user.set_password(None)
        assert user.save()

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

        user.set_password(pw2)
        assert user.save()

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
        user.refresh()
        assert user.last_login_fmt == user.last_login.strftime(FMT_STRFTIME)

    @staticmethod
    def test_last_login_epoch(gen_user):
        user = gen_user()
        assert user.last_login_epoch is None
        assert user.last_login_epoch_ms is None
        user.refresh()
        assert user.last_login_epoch <= (
            user.last_login - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert user.last_login_epoch_ms == 1000 * user.last_login_epoch
