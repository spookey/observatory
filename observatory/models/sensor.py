from logging import getLogger

from observatory.database import CommonMixin, CreatedMixin, Model
from observatory.models.point import Point
from observatory.start.extensions import DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Sensor(CommonMixin, CreatedMixin, Model):
    points = DB.relationship(
        'Point',
        backref=DB.backref('sensor', lazy=True),
        order_by='Point.created.desc()',
        cascade='all,delete-orphan',
        lazy=True,
    )

    @property
    def query_points(self):
        return Point.query.with_parent(self).order_by(Point.created.desc())

    @property
    def query_points_outdated(self):
        return Point.query_outdated(self.query_points)

    @property
    def length(self):
        return self.query_points.count()

    @property
    def latest(self):
        return self.query_points.first()

    def cleanup(self):
        query = self.query_points_outdated
        LOG.info('cleanup "%d" outdated points', query.count())

        return all(point.delete() for point in query.all())

    def append(self, value):
        self.cleanup()
        LOG.info('creating new point with "%f" for "%s"', value, self.slug)

        return Point.create(sensor=self, value=value)
