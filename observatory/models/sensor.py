from logging import getLogger

from observatory.database import CommonMixin, CreatedMixin, Model, SortMixin
from observatory.models.point import Point
from observatory.start.extensions import DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Sensor(CommonMixin, SortMixin, CreatedMixin, Model):
    points = DB.relationship(
        'Point',
        backref=DB.backref('sensor', lazy=True),
        order_by='Point.created.desc()',
        cascade='all,delete-orphan',
        lazy=True,
    )
    values = DB.relationship(
        'Value',
        backref=DB.backref('sensor', lazy=True),
        order_by='Value.idx.asc()',
        cascade='all,delete-orphan',
        lazy=True,
    )

    sticky = DB.Column(
        DB.Boolean(),
        nullable=False,
        default=False,
    )

    @property
    def active(self):
        return any(self.mapping_active)

    @classmethod
    def query_sticky(cls, sticky=True, query=None):
        query = query if query is not None else cls.query
        return query.filter(cls.sticky == sticky)

    @property
    def query_points(self):
        return Point.query_sorted(Point.query.with_parent(self))

    @property
    def length(self):
        return self.query_points.count()

    @property
    def latest(self):
        return self.query_points.first()

    def cleanup(self, _commit=True):
        query = Point.query_sorted(Point.query_outdated())
        if self.sticky:
            query = query.offset(1)

        LOG.info('cleanup "%d" outdated points', query.count())

        return all(point.delete(_commit=_commit) for point in query.all())

    def append(self, *, user, value, _commit=True):
        self.cleanup()
        LOG.info('creating new point with "%f" for "%s"', value, self.slug)

        return Point.create(
            sensor=self, user=user, value=value, _commit=_commit
        )
