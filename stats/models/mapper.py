from enum import Enum

from sqlalchemy import and_

from stats.database import BaseModel, CreatedMixin
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class EnumAxis(Enum):
    LEFT = 1
    RIGHT = 2


class EnumCast(Enum):
    NATURAL = 1
    INTEGER = 2
    BOOLEAN = 4


class EnumHorizon(Enum):
    NORMAL = 1
    INVERT = 2


class Mapper(CreatedMixin, BaseModel):
    prompt_pime = DB.Column(
        DB.Integer(), DB.ForeignKey('prompt.prime'), primary_key=True
    )
    sensor_pime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), primary_key=True
    )
    active = DB.Column(
        DB.Boolean(), nullable=False, default=True
    )
    axis = DB.Column(
        DB.Enum(EnumAxis), nullable=False, default=EnumAxis.LEFT
    )
    cast = DB.Column(
        DB.Enum(EnumCast), nullable=False, default=EnumCast.NATURAL
    )
    horizon = DB.Column(
        DB.Enum(EnumHorizon), nullable=False, default=EnumHorizon.NORMAL
    )

    @classmethod
    def by_commons(cls, prompt, sensor):
        return cls.query.filter(and_(
            cls.prompt == prompt,
            cls.sensor == sensor,
        )).first()
