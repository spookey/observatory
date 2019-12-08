from flask import url_for
from flask_login import current_user
from pytest import mark

ENDPOINT = 'user.logout'


@mark.usefixtures('session')
class TestUserLogout:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/logout'

    @staticmethod
    def test_no_user(visitor):
        assert current_user.is_authenticated is False
        visitor(ENDPOINT, code=401)
        assert current_user.is_authenticated is False

    @staticmethod
    def test_with_user(visitor, gen_user_loggedin):
        user = gen_user_loggedin()
        assert user == current_user
        assert current_user.is_authenticated is True
        res = visitor(ENDPOINT, code=302)
        assert res.request.headers['Location'] == url_for(
            'main.index', _external=True
        )
        assert current_user.is_authenticated is False
