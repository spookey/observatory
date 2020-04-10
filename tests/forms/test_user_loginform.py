from datetime import datetime

from flask_login import current_user
from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.user import LoginForm
from tests.conftest import USER_NAME, USER_PASS


@mark.usefixtures('session', 'ctx_app')
class TestLoginForm:

    @staticmethod
    def test_basic_fields():
        form = LoginForm()
        assert form.username is not None
        assert form.password is not None
        assert form.remember is not None
        assert form.submit is not None

    @staticmethod
    def test_submit_button():
        form = LoginForm()
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'user_enter'

    @staticmethod
    def test_empty_user():
        form = LoginForm()
        assert form.user is None

    @staticmethod
    def test_empty_invalid():
        form = LoginForm()
        assert form.validate() is False
        assert form.action() is None
        assert form.user is None

    @staticmethod
    def test_not_found():
        form = LoginForm(username=USER_NAME, password=USER_PASS)
        assert form.validate() is False
        assert 'unknown' in form.username.errors[-1].lower()

    @staticmethod
    def test_wrong_password(gen_user):
        gen_user(username=USER_NAME, password=USER_PASS)
        form = LoginForm(username=USER_NAME, password=USER_PASS + USER_PASS)
        assert form.validate() is False
        assert 'wrong' in form.password.errors[-1].lower()

    @staticmethod
    def test_inactive(gen_user):
        gen_user(username=USER_NAME, password=USER_PASS, active=False)
        form = LoginForm(username=USER_NAME, password=USER_PASS)
        assert form.validate() is False
        assert 'blocked' in form.username.errors[-1].lower()

    @staticmethod
    def test_login_validate(gen_user):
        user = gen_user(username=USER_NAME, password=USER_PASS)
        form = LoginForm(username=USER_NAME, password=USER_PASS)
        assert form.validate() is True
        assert form.user == user

    @staticmethod
    def test_login_action(gen_user):
        user = gen_user(username=USER_NAME, password=USER_PASS)
        form = LoginForm(username=USER_NAME, password=USER_PASS)
        assert form.validate() is True
        assert form.action() == user
        assert form.user == user
        assert current_user == user
        assert user.is_authenticated is True

    @staticmethod
    def test_last_login(gen_user):
        start = datetime.utcnow()
        user = gen_user(username=USER_NAME, password=USER_PASS)
        assert user.last_login is None

        form = LoginForm(username=USER_NAME, password=USER_PASS)
        assert form.validate() is True
        assert form.action() == user

        assert start <= user.last_login
        assert user.last_login <= datetime.utcnow()
