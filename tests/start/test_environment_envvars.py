from importlib import reload
from os import path

from observatory.start import environment


def test_database(monkeypatch):
    db_path = path.abspath(path.join(
        environment.ROOT_DIR, 'database_dev.sqlite'
    ))
    assert environment.DATABASE == 'sqlite://'
    assert environment.DATABASE_DEV == f'sqlite:///{db_path}'

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


def test_bcrypt_log_rounds(monkeypatch):
    assert environment.BCRYPT_LOG_ROUNDS == 13

    monkeypatch.setenv('BCRYPT_LOG_ROUNDS', '42')
    reload(environment)

    assert environment.BCRYPT_LOG_ROUNDS == 42


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
    assert environment.TITLE == 'Status'

    monkeypatch.setenv('TITLE', '🕹')
    reload(environment)

    assert environment.TITLE == '🕹'


def test_language(monkeypatch):
    assert environment.HTML_LANG == 'en'

    monkeypatch.setenv('HTML_LANG', '🗻')
    reload(environment)

    assert environment.HTML_LANG == '🗻'


def test_favicon(monkeypatch):
    assert environment.FAVICON == 'logo.png'

    monkeypatch.setenv('FAVICON', '💥')
    reload(environment)

    assert environment.FAVICON == '💥'


def test_fmt_fields(monkeypatch):
    assert environment.FMT_STRFTIME == '%d.%m.%Y %H:%M:%S UTC'
    assert environment.FMT_MOMENT == 'DD. MMM YYYY HH:mm:ss'

    monkeypatch.setenv('FMT_STRFTIME', '⏰')
    monkeypatch.setenv('FMT_MOMENT', '⏱')
    reload(environment)

    assert environment.FMT_STRFTIME == '⏰'
    assert environment.FMT_MOMENT == '⏱'


def test_taglines(monkeypatch):
    for num, line in enumerate(environment.TAGLINES):
        assert environment.TAGLINES[num] == line

        monkeypatch.setenv(f'TAGLINE_{1 + num:02d}', '*️⃣')
        reload(environment)

        assert environment.TAGLINES[num] == '*️⃣'
