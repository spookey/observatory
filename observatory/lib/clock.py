from datetime import datetime, timedelta

from observatory.start.environment import BACKLOG_DAYS, FMT_STRFTIME


def epoch_seconds(stamp):
    return int((stamp - datetime.utcfromtimestamp(0)).total_seconds())


def epoch_milliseconds(stamp):
    return 1000 * epoch_seconds(stamp)


def is_outdated(stamp, days=BACKLOG_DAYS):
    return stamp <= datetime.utcnow() - timedelta(days=days)


def time_format(stamp, fmt=FMT_STRFTIME):
    if stamp is None:
        return ''
    return stamp.strftime(fmt)
