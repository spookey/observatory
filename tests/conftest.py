from json import loads

from bs4 import BeautifulSoup
from flask import url_for
from pytest import fixture

from stats.app import create_app
from stats.models.sensor import Sensor
from stats.models.user import User
from stats.start.config import TestingConfig
from stats.start.extensions import DB as _db

# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments


@fixture(scope='session')
def app():
    _app = create_app(TestingConfig)
    with _app.app_context():
        yield _app


@fixture(scope='function')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db
    _db.session.close()
    _db.drop_all()


@fixture(scope='function')
def session(db):
    _connection = db.engine.connect()
    _transaction = _connection.begin()
    _session = db.create_scoped_session(
        options={'bind': _connection, 'binds': {}}
    )
    db.session = _session

    yield _session
    _transaction.rollback()
    _connection.close()
    _session.remove()


@fixture(scope='session')
def ctx_app(app):
    with app.test_request_context():
        yield app


@fixture(scope='function')
def client(ctx_app):
    with ctx_app.test_client() as cli:
        yield cli


def _visitor(client):
    def make(
            endpoint,
            *,
            code=200,
            data=None,
            headers=None,
            method='get',
            params=None,
            query_string=None
    ):
        params = params if params is not None else {}
        url = url_for(endpoint, **params)

        caller = {
            'get': client.get,
            'post': client.post,
            'put': client.put,
        }.get(method.lower())

        request = caller(
            url, data=data, headers=headers, query_string=query_string
        )
        assert request.status_code == code

        def res():
            pass

        res.url = url
        res.request = request
        res.page = request.get_data(as_text=True)

        res.soup = BeautifulSoup(res.page, 'html.parser')

        try:
            res.json = loads(res.page)
        except ValueError:
            res.json = None

        return res

    yield make


@fixture(scope='function')
def visitor(client):
    yield from _visitor(client)


###
# DB helpers


SENSOR_NAME = 'test'
SENSOR_TITLE = 'Test Sensor'
SENSOR_DESCRIPTION = 'Some sensor just for UnitTests'


@fixture(scope='function')
def gen_sensor():
    def make(
            name=SENSOR_NAME,
            title=SENSOR_TITLE,
            description=SENSOR_DESCRIPTION,
            **kwargs
    ):
        return Sensor.create(
            name=name, title=title, description=description,
            **kwargs
        )

    yield make


USER_NAME = 'user'
USER_PASS = 'secret'


@fixture(scope='function')
def gen_user():
    def make(username=USER_NAME, password=USER_PASS, **kwargs):
        return User.create(
            username=username,
            password=password,
            **kwargs
        )

    yield make
