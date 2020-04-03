from base64 import b64encode

from pytest import mark
from werkzeug.test import create_environ
from werkzeug.wrappers import Request

from observatory.views.user import request_loader
from tests.conftest import USER_NAME, USER_PASS


def _auth_header(username, password):
    return (
        'authorization',
        b'basic ' + b64encode(':'.join((username, password)).encode())
    )


def _request(*headers):
    return Request(create_environ(headers=headers))


@mark.usefixtures('session')
class TestRequestLoader:

    @staticmethod
    def test_request_loader_empty():
        assert request_loader(_request()) is None

    @staticmethod
    def test_request_loader_no_user():
        assert request_loader(
            _request(_auth_header(USER_NAME, USER_PASS))
        ) is None

    @staticmethod
    def test_request_loader(gen_user):
        user = gen_user(username=USER_NAME, password=USER_PASS)
        assert request_loader(
            _request(_auth_header(USER_NAME, USER_PASS))
        ) == user
