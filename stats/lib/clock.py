from datetime import datetime, timedelta

from stats.start.environment import BACKLOG_DAYS


def epoch_seconds(stamp):
    return int((stamp - datetime.utcfromtimestamp(0)).total_seconds())


def epoch_milliseconds(stamp):
    return 1000 * epoch_seconds(stamp)


def is_outdated(stamp, days=BACKLOG_DAYS):
    return stamp <= datetime.utcnow() - timedelta(days=days)
