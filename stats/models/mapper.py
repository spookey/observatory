from enum import Enum

from sqlalchemy import and_

from stats.database import BaseModel, CreatedMixin
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class EnumColor(Enum):
    GRAY = 0x969896
    RED = 0xc82829
    ORANGE = 0xf5871f
    YELLOW = 0xeab700
    GREEN = 0x718c00
    TURQUOISE = 0x3e999f
    BLUE = 0x4271ae
    PURPLE = 0x8959a8
    BROWN = 0xa3685a


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
    color = DB.Column(
        DB.Enum(EnumColor), nullable=False, default=EnumColor.GRAY
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
