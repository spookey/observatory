from sqlalchemy.ext.hybrid import hybrid_property

from observatory.database import CreatedMixin, Model
from observatory.lib.clock import is_outdated
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

    def translate(self, *, horizon, convert, elevate=1.0, numeric=False):
        _flip = -1 if horizon == EnumHorizon.INVERT else +1
        value = float(_flip * self.value)

        if convert == EnumConvert.BOOLEAN:
            value = bool(round(value))
            if not numeric:
                return value
            return (_flip * elevate) if value else 0.0

        if convert == EnumConvert.INTEGER:
            return round(elevate * value)

        return float(elevate * value)

    def translate_map(self, mapper, numeric=False):
        return self.translate(
            horizon=mapper.horizon,
            convert=mapper.convert,
            elevate=mapper.elevate,
            numeric=numeric,
        )
