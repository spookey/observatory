from datetime import datetime
from logging import getLogger

from stats.database import Model
from stats.models.point import Point
from stats.start.extensions import DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Sensor(Model):
    name = DB.Column(DB.String(length=64), unique=True, nullable=False)
    title = DB.Column(DB.String(length=512), nullable=False)
    description = DB.Column(DB.String(length=4096), nullable=False)
    created = DB.Column(
        DB.DateTime(), nullable=False, default=datetime.utcnow
    )

    points = DB.relationship(
        'Point',
        backref=DB.backref('sensor', lazy=True),
        order_by=Point.stamp.desc(),
        cascade='all,delete',
        lazy=True,
    )

    @classmethod
    def by_name(cls, name):
        return cls.query.filter(cls.name == name).first()

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
