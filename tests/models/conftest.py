from datetime import datetime, timedelta

from pytest import fixture

from observatory.models.point import Point
from observatory.start.environment import BACKLOG_DAYS


@fixture(scope='function')
def gen_points_batch(gen_sensor, gen_user):
    def make(
        sensor=None,
        user=None,
        start=None,
        old=5,
        new=5,
    ):

        sensor = sensor if sensor is not None else gen_sensor()
        user = user if user is not None else gen_user()
        start = start if start is not None else datetime.utcnow()

        olds = [
            Point.create(
                sensor=sensor,
                user=user,
                value=value,
                created=start - timedelta(days=BACKLOG_DAYS, hours=value),
            )
            for value in range(old)
        ]
        news = [
            Point.create(
                sensor=sensor,
                user=user,
                value=value,
                created=start + timedelta(days=BACKLOG_DAYS, hours=value),
            )
            for value in range(new)
        ]

        return olds, news, [fl for at in (olds, news) for fl in at]

    yield make
