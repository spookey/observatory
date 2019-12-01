from pytest import fixture

from stats.app import create_app
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

###
# DB helpers


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

    return make
