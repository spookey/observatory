from importlib import reload
from os import path

from stats.start import environment


def test_database(monkeypatch):
    assert environment.DATABASE == 'sqlite://'
    assert environment.DATABASE_DEV == 'sqlite:///{}'.format(
        path.abspath(path.join(
            environment.ROOT_DIR, 'database_dev.sqlite'
        ))
    )

    monkeypatch.setenv('DATABASE', '💾')
    monkeypatch.setenv('DATABASE_DEV', '📼')
    reload(environment)

    assert environment.DATABASE == '💾'
    assert environment.DATABASE_DEV == '📼'


def test_loglevel(monkeypatch):
    assert environment.LOG_LVL == 'info'

    monkeypatch.setenv('LOG_LVL', '🛎')
    reload(environment)

    assert environment.LOG_LVL == '🛎'


def test_secret(monkeypatch):
    assert environment.SECRET_BASE == environment.ROOT_DIR
    assert environment.SECRET_FILE == 'secret.key'

    monkeypatch.setenv('SECRET_BASE', '📌')
    monkeypatch.setenv('SECRET_FILE', '✏️')
    reload(environment)

    assert environment.SECRET_BASE == '📌'
    assert environment.SECRET_FILE == '✏️'


def test_csrf_strict(monkeypatch):
    assert environment.CSRF_STRICT is True

    monkeypatch.setenv('CSRF_STRICT', '🍉')
    reload(environment)

    assert environment.CSRF_STRICT is True


def test_backlog_days(monkeypatch):
    assert environment.BACKLOG_DAYS == 14

    monkeypatch.setenv('BACKLOG_DAYS', '1337')
    reload(environment)

    assert environment.BACKLOG_DAYS == 1337


def test_title(monkeypatch):
    assert environment.TITLE == environment.APP_NAME

    monkeypatch.setenv('TITLE', '🕹')
    reload(environment)

    assert environment.TITLE == '🕹'


def test_language(monkeypatch):
    assert environment.HTML_LANG == 'en'

    monkeypatch.setenv('HTML_LANG', '🗻')
    reload(environment)

    assert environment.HTML_LANG == '🗻'


def test_favicon(monkeypatch):
    assert environment.FAVICON == 'hex.png'

    monkeypatch.setenv('FAVICON', '💥')
    reload(environment)

    assert environment.FAVICON == '💥'
