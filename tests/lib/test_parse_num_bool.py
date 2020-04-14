from observatory.lib.parse import parse_num_bool

NUM_TRUTHY = (1, 1.0, 1.1, 2.3)
NUM_WRONG = ('test', None, Exception)


def test_simple():
    for val in NUM_TRUTHY:
        assert parse_num_bool(val, warn=False) is True
    assert parse_num_bool(0, warn=False) is False


def test_explicit():
    assert parse_num_bool(True, fallback=None, warn=False) is True
    assert parse_num_bool(False, fallback=None, warn=False) is False


def test_fallback():
    for val in NUM_WRONG:
        assert parse_num_bool(val, fallback=None, warn=False) is None
        assert parse_num_bool(val, fallback=True, warn=False) is True


def test_silent(caplog):
    assert parse_num_bool(None, fallback=False, warn=False) is False
    assert not caplog.records


def test_logging(caplog):
    assert parse_num_bool(None, fallback=True, warn=True) is True

    exc, wrn = caplog.records
    assert exc.levelname == 'ERROR'
    assert wrn.levelname == 'WARNING'

    assert 'NoneType' in exc.message
    assert 'fallback' in wrn.message
    assert 'True' in wrn.message
