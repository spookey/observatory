from observatory.start.environment import MIGR_DIR
from observatory.start.extensions import (
    BCRYPT, CSRF_PROTECT, DB, LOGIN_MANAGER, MIGRATE, REST
)


class TestExtensions:

    @staticmethod
    def test_for_bcrypt(app):
        assert BCRYPT is not None
        assert app.config['BCRYPT_LOG_ROUNDS'] is not None

    @staticmethod
    def test_for_csrf(app):
        assert CSRF_PROTECT is not None
        assert CSRF_PROTECT == app.extensions['csrf']
        assert app.config['WTF_CSRF_CHECK_DEFAULT'] is True

    @staticmethod
    def test_for_db(app):
        assert DB is not None
        assert DB == app.extensions['sqlalchemy'].db
        assert DB.engine.url.database is None  # memory db

    @staticmethod
    def test_for_login_manager(app):
        assert LOGIN_MANAGER is not None
        assert app.login_manager == LOGIN_MANAGER

    # pylint: disable=invalid-name

    @staticmethod
    def test_for_migrate(app, db):
        assert MIGRATE is not None
        assert MIGRATE == app.extensions['migrate'].migrate
        assert MIGRATE.directory == MIGR_DIR
        assert MIGRATE.db == db

    @staticmethod
    def test_for_rest(app):
        assert REST is not None
        assert REST.prefix == '/api'
        assert REST.decorators == [CSRF_PROTECT.exempt]
        assert REST.serve_challenge_on_401 is True
        for ep in REST.endpoints:
            assert ep in app.view_functions
