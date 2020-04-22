from sqlalchemy.ext.hybrid import hybrid_property

from observatory.database import CreatedMixin, Model
from observatory.lib.clock import is_outdated
from observatory.lib.parse import parse_num_bool
from observatory.models.mapper import EnumConvert, EnumHorizon
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

    def convert(self, horizon, convert, numeric=False):
        value = float(self.value)

        if horizon == EnumHorizon.INVERT:
            value = -1 * value

        if convert == EnumConvert.BOOLEAN:
            value = parse_num_bool(value)
            if not numeric:
                return value
            if not value:
                return 0
            return -1 if horizon == EnumHorizon.INVERT else 1

        if convert == EnumConvert.INTEGER:
            return round(value)

        return value
