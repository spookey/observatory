from sqlalchemy.ext.hybrid import hybrid_property

from observatory.database import CreatedMixin, Model
from observatory.lib.clock import is_outdated
from observatory.lib.parse import parse_int, parse_num_bool
from observatory.models.mapper import EnumConvert
from observatory.start.environment import BACKLOG_DAYS
from observatory.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Point(CreatedMixin, Model):
    value = DB.Column(DB.Float(), nullable=False)

    sensor_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), nullable=False,
    )

    @hybrid_property
    def outdated(self):
        return is_outdated(self.created, BACKLOG_DAYS)

    @classmethod
    def query_outdated(cls, query=None):
        query = query if query is not None else cls.query
        return query.filter(cls.outdated)

    def convert(self, conv):
        if conv == EnumConvert.BOOLEAN:
            return parse_num_bool(self.value)
        if conv == EnumConvert.INTEGER:
            return parse_int(self.value)
        if conv == EnumConvert.NATURAL:
            return float(self.value)
        return None
