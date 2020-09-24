from flask import url_for
from flask_login import current_user
from pytest import mark

from tests.conftest import USER_PASS

ENDPOINT = 'user.login'


@mark.usefixtures('session')
class TestUserLogin:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/login'

    @staticmethod
    def test_basic_form(visitor):
        res = visitor(ENDPOINT)
        form = res.soup.select('form')[-1]
        assert form.attrs['method'].lower() == 'post'
        assert form.attrs['action'] == url_for(ENDPOINT, _external=True)

    @staticmethod
    def test_form_fields(visitor):
        res = visitor(ENDPOINT)
        form = res.soup.select('form')[-1]
        fields = [
            (inpt.attrs.get('name'), inpt.attrs.get('type'))
            for inpt in form.select('input,button')
        ]
        assert fields == [
            ('username', 'text'),
            ('password', 'password'),
            ('remember', 'checkbox'),
            ('submit', 'submit'),
        ]

    @staticmethod
    def test_form_wrong(visitor, gen_user):
        assert current_user.is_authenticated is False
        user = gen_user()
        res = visitor(
            ENDPOINT,
            method='post',
            data={
                'username': user.username,
                'password': user.pw_hash,
                'remember': True,
                'submit': True,
            },
        )

        form = res.soup.select('form')[-1]
        for sel, exp in [
            ('#username', user.username),
            ('#password', ''),
            ('#remember', 'True'),
        ]:
            assert form.select(sel)[-1].attrs['value'] == exp
        assert current_user.is_authenticated is False

    @staticmethod
    def test_form_login(visitor, gen_user):
        assert current_user.is_authenticated is False
        user = gen_user(password=USER_PASS)
        home_url = url_for('main.index', _external=True)

        res = visitor(
            ENDPOINT,
            method='post',
            data={
                'username': user.username,
                'password': USER_PASS,
                'remember': True,
                'submit': True,
            },
            code=302,
        )

        assert res.request.headers['Location'] == home_url
        assert current_user == user
        assert current_user.is_authenticated is True
        assert current_user.username == user.username

    @staticmethod
    def test_form_login_next(visitor, gen_user):
        assert current_user.is_authenticated is False
        user = gen_user(password=USER_PASS)
        next_url = url_for('side.favicon', _external=True)

        res = visitor(
            ENDPOINT,
            method='post',
            data={
                'username': user.username,
                'password': USER_PASS,
                'remember': True,
                'submit': True,
            },
            query_string={'next': next_url},
            code=302,
        )

        assert res.request.headers['Location'] == next_url
        assert current_user.is_authenticated is True
