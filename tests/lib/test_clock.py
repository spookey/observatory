from datetime import datetime, timedelta

from stats.lib.clock import (
    epoch_milliseconds, epoch_seconds, is_outdated, time_format
)
from stats.start.environment import FMT_STRFTIME


def test_epoch_from_ts():
    for value in (60 * num for num in range(60)):
        stamp = datetime.utcfromtimestamp(value)

        assert epoch_seconds(stamp) == value
        assert epoch_milliseconds(stamp) == 1000 * value


def test_epoch_now():
    start = datetime.utcnow()
    res = epoch_seconds(start)
    assert res <= (
        start - datetime.utcfromtimestamp(0)
    ).total_seconds()


def test_is_outdated():
    now = datetime.utcnow()
    days = 3

    assert is_outdated(now - timedelta(days=0), days=days) is False
    assert is_outdated(now - timedelta(days=1), days=days) is False
    assert is_outdated(now - timedelta(days=2), days=days) is False
    assert is_outdated(now - timedelta(days=3), days=days) is True
    assert is_outdated(now - timedelta(days=4), days=days) is True
    assert is_outdated(now - timedelta(days=5), days=days) is True


def test_time_format():
    now = datetime.utcnow()

    assert time_format(None) == ''
    assert time_format(now, fmt='') == ''
    assert time_format(now, fmt='%Y') == f'{now.year}'
    assert time_format(now, fmt='%-m') == f'{now.month}'
    assert time_format(now) == now.strftime(FMT_STRFTIME)
