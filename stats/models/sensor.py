from logging import getLogger

from stats.database import CommonMixin, CreatedMixin, Model
from stats.models.display import Display
from stats.models.point import Point
from stats.start.extensions import DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Sensor(CommonMixin, CreatedMixin, Model):
    points = DB.relationship(
        Point,
        backref=DB.backref('sensor', lazy=True),
        order_by=Point.stamp.desc(),
        cascade='all,delete',
        lazy=True,
    )

    displays = DB.relationship(
        Display,
        primaryjoin='Sensor.prime == Display.sensor_pime',
        backref=DB.backref('sensor', lazy=True),
        lazy=True,
    )

    @classmethod
    def query_points_outdated(cls):
        return Point.query_outdated(Point.query.join(cls))

    @classmethod
    def cleanup(cls):
        query = cls.query_points_outdated()
        LOG.info('cleanup "%d" outdated points', query.count())

        for point in query.all():
            point.delete()

    def append(self, value):
        self.cleanup()
        return Point.create(sensor=self, value=value)
