from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from stats.models.user import User


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

        assert one.get_id() == '{}'.format(one.prime)
        assert two.get_id() == '{}'.format(two.prime)

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
    def test_update_last_login(gen_user):
        start = datetime.utcnow()
        user = gen_user()

        assert user.last_login is None

        user.set_last_login()
        assert user.save()

        assert start <= user.last_login
        assert user.last_login <= datetime.utcnow()
