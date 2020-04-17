from enum import Enum

from sqlalchemy import and_

from observatory.database import BaseModel, CreatedMixin, SortMixin
from observatory.start.extensions import DB


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

    @property
    def color(self):
        return f'#{self.value:6x}'

    @classmethod
    def from_color(cls, val):
        try:
            return cls(int(val.lstrip('#'), 16))
        except (AttributeError, ValueError):
            return cls.GRAY


class EnumConvert(Enum):
    NATURAL = 1
    INTEGER = 2
    BOOLEAN = 4


class EnumHorizon(Enum):
    NORMAL = 1
    INVERT = 2


# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Mapper(SortMixin, CreatedMixin, BaseModel):
    prompt_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('prompt.prime'), primary_key=True
    )
    sensor_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), primary_key=True
    )
    active = DB.Column(
        DB.Boolean(), nullable=False, default=True
    )
    color = DB.Column(
        DB.Enum(EnumColor), nullable=False, default=EnumColor.GRAY
    )
    convert = DB.Column(
        DB.Enum(EnumConvert), nullable=False, default=EnumConvert.NATURAL
    )
    horizon = DB.Column(
        DB.Enum(EnumHorizon), nullable=False, default=EnumHorizon.NORMAL
    )

    prompt = DB.relationship(
        'Prompt',
        primaryjoin='Mapper.prompt_prime == Prompt.prime',
        backref=DB.backref(
            'mapping',
            order_by='Mapper.sortkey.desc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        lazy=True,
    )
    sensor = DB.relationship(
        'Sensor',
        primaryjoin='Mapper.sensor_prime == Sensor.prime',
        backref=DB.backref(
            'mapping',
            order_by='Mapper.sortkey.desc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        lazy=True,
    )

    prompt_active = DB.relationship(
        'Prompt',
        primaryjoin='''and_(
            Mapper.active.is_(True),
            Mapper.prompt_prime == Prompt.prime
        )''',
        backref=DB.backref(
            'mapping_active',
            order_by='Mapper.sortkey.desc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        lazy=True,
    )
    sensor_active = DB.relationship(
        'Sensor',
        primaryjoin='''and_(
            Mapper.active.is_(True),
            Mapper.sensor_prime == Sensor.prime
        )''',
        backref=DB.backref(
            'mapping_active',
            order_by='Mapper.sortkey.desc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        lazy=True,
    )

    @classmethod
    def by_commons(cls, prompt, sensor):
        return cls.query.filter(and_(
            cls.prompt == prompt,
            cls.sensor == sensor,
        )).first()
