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
    assert environment.TITLE == 'Observatory'

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
    assert environment.FMT_MOMENT_DEFAULT == 'DD. MMM YYYY HH:mm:ss'
    assert environment.FMT_MOMENT_MSECOND == 'DD. MMM YYYY HH:mm:SS'
    assert environment.FMT_MOMENT_SECOND == 'DD. MMM YYYY HH:mm:ss'
    assert environment.FMT_MOMENT_MINUTE == 'DD. MMM YYYY HH:mm:ss'
    assert environment.FMT_MOMENT_HOUR == 'DD. MMM YYYY HH:mm'
    assert environment.FMT_MOMENT_DAY == 'DD. MMM YYYY HH:mm'
    assert environment.FMT_MOMENT_WEEK == 'DD. MMM YYYY'
    assert environment.FMT_MOMENT_MONTH == 'DD. MMM YYYY'
    assert environment.FMT_MOMENT_QUARTER == 'MMM YYYY'
    assert environment.FMT_MOMENT_YEAR == 'MMM YYYY'

    monkeypatch.setenv('FMT_STRFTIME', '⏰')
    monkeypatch.setenv('FMT_MOMENT_DEFAULT', '⏱')
    monkeypatch.setenv('FMT_MOMENT_MSECOND', '⏱ msecond')
    monkeypatch.setenv('FMT_MOMENT_SECOND', '⏱ second')
    monkeypatch.setenv('FMT_MOMENT_MINUTE', '⏱ minute')
    monkeypatch.setenv('FMT_MOMENT_HOUR', '⏱ hour')
    monkeypatch.setenv('FMT_MOMENT_DAY', '⏱ day')
    monkeypatch.setenv('FMT_MOMENT_WEEK', '⏱ week')
    monkeypatch.setenv('FMT_MOMENT_MONTH', '⏱ month')
    monkeypatch.setenv('FMT_MOMENT_QUARTER', '⏱ quarter')
    monkeypatch.setenv('FMT_MOMENT_YEAR', '⏱ year')
    reload(environment)

    assert environment.FMT_STRFTIME == '⏰'
    assert environment.FMT_MOMENT_DEFAULT == '⏱'
    assert environment.FMT_MOMENT_MSECOND == '⏱ msecond'
    assert environment.FMT_MOMENT_SECOND == '⏱ second'
    assert environment.FMT_MOMENT_MINUTE == '⏱ minute'
    assert environment.FMT_MOMENT_HOUR == '⏱ hour'
    assert environment.FMT_MOMENT_DAY == '⏱ day'
    assert environment.FMT_MOMENT_WEEK == '⏱ week'
    assert environment.FMT_MOMENT_MONTH == '⏱ month'
    assert environment.FMT_MOMENT_QUARTER == '⏱ quarter'
    assert environment.FMT_MOMENT_YEAR == '⏱ year'


def test_api_plot_refresh_ms(monkeypatch):
    assert environment.API_PLOT_REFRESH_MS == 1500

    monkeypatch.setenv('API_PLOT_REFRESH_MS', '23')
    reload(environment)

    assert environment.API_PLOT_REFRESH_MS == 23


def test_taglines(monkeypatch):
    for num, line in enumerate(environment.TAGLINES):
        assert environment.TAGLINES[num] == line

        monkeypatch.setenv(f'TAGLINE_{1 + num:02d}', '*️⃣')
        reload(environment)

        assert environment.TAGLINES[num] == '*️⃣'


def test_icons(monkeypatch):
    def _check(elems, expect=None):
        for key, val in elems.items():
            value = expect if expect is not None else val
            assert value
            assert isinstance(value, str)
            assert elems[key] == value

    _check(environment.ICON)

    for key in environment.ICON:
        monkeypatch.setenv(f'ICON_{key.upper()}', '🌭')
    reload(environment)

    _check(environment.ICON, '🌭')
