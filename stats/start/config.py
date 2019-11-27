from os import path, urandom

from stats.start.environment import (
    APP_NAME, CSRF_STRICT, DATABASE, DATABASE_DEV, HTML_LANG, SECRET_BASE,
    SECRET_FILE, TITLE
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
    DEBUG = False
    HTML_LANG = HTML_LANG
    SECRET_KEY = secret_key()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    TITLE = TITLE
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = CSRF_STRICT


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_DEV


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE
