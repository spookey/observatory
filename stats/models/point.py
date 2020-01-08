from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from stats.database import Model
from stats.lib.clock import epoch_milliseconds, epoch_seconds, is_outdated
from stats.start.environment import BACKLOG_DAYS
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Point(Model):
    value = DB.Column(DB.Float(), nullable=False)
    stamp = DB.Column(
        DB.DateTime(), nullable=False, default=datetime.utcnow
    )

    sensor_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), nullable=False
    )

    @hybrid_property
    def epoch(self):
        return epoch_seconds(self.stamp)

    @hybrid_property
    def epoch_ms(self):
        return epoch_milliseconds(self.stamp)

    @hybrid_property
    def outdated(self):
        return is_outdated(self.stamp, BACKLOG_DAYS)

    @classmethod
    def query_outdated(cls, query=None):
        query = query if query is not None else cls.query
        return query.filter(cls.outdated)
