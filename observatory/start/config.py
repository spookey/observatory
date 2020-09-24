from os import path, urandom

from observatory.start.environment import (
    APP_NAME,
    BCRYPT_LOG_ROUNDS,
    CSRF_STRICT,
    DATABASE,
    DATABASE_DEV,
    FAVICON,
    HTML_LANG,
    ICON,
    SECRET_BASE,
    SECRET_FILE,
    TITLE,
)


def secret_key(base=SECRET_BASE, filename=SECRET_FILE):
    location = path.abspath(path.join(base, filename))
    if not path.exists(location):
        secret = urandom(1024)
        with open(location, 'wb') as handle:
            handle.write(secret)
        return secret
    with open(location, 'rb') as handle:
        return handle.read()


# pylint: disable=too-few-public-methods


class BaseConfig:
    APP_NAME = APP_NAME
    BCRYPT_LOG_ROUNDS = BCRYPT_LOG_ROUNDS
    DEBUG = False
    FAVICON = FAVICON
    HTML_LANG = HTML_LANG
    ICON = ICON
    SECRET_KEY = secret_key()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    TITLE = TITLE
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = CSRF_STRICT

    HTTP_BASIC_AUTH_REALM = TITLE
    RESTFUL_JSON = {'indent': None, 'sort_keys': True}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_DEV
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 5
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE
