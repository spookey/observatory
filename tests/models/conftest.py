from datetime import datetime, timedelta

from pytest import fixture

from stats.models.point import Point
from stats.start.environment import BACKLOG_DAYS


@fixture(scope='function')
def gen_points_batch():
    def make(
            sensor,
            start=None,
            old=5,
            new=5,
    ):
        start = start if start is not None else datetime.utcnow()

        olds = [
            Point.create(
                sensor=sensor, value=value,
                created=start - timedelta(days=BACKLOG_DAYS, hours=value)
            )
            for value in range(old)
        ]
        news = [
            Point.create(
                sensor=sensor, value=value,
                created=start + timedelta(days=BACKLOG_DAYS, hours=value)
            )
            for value in range(new)
        ]

        return olds, news, [fl for at in (olds, news) for fl in at]

    yield make
