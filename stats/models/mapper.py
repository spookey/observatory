from datetime import datetime
from enum import Enum

from stats.database import BaseModel
from stats.lib.clock import time_format
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


class Mapper(BaseModel):
    prompt_pime = DB.Column(
        DB.Integer(), DB.ForeignKey('prompt.prime'), primary_key=True
    )
    sensor_pime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), primary_key=True
    )
    created = DB.Column(
        DB.DateTime(), nullable=False, default=datetime.utcnow
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
        return cls.query.filter(
            cls.prompt == prompt,
            cls.sensor == sensor,
        ).first()

    @property
    def created_fmt(self):
        return time_format(self.created)
