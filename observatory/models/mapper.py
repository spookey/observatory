from enum import Enum

from sqlalchemy import and_

from observatory.database import BaseModel, CreatedMixin
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


class EnumCast(Enum):
    NATURAL = 1
    INTEGER = 2
    BOOLEAN = 4


class EnumHorizon(Enum):
    NORMAL = 1
    INVERT = 2


def _next_sortkey():
    return 1 + Mapper.query.count()

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Mapper(CreatedMixin, BaseModel):
    prompt_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('prompt.prime'), primary_key=True
    )
    sensor_prime = DB.Column(
        DB.Integer(), DB.ForeignKey('sensor.prime'), primary_key=True
    )
    active = DB.Column(
        DB.Boolean(), nullable=False, default=True
    )
    sortkey = DB.Column(
        DB.Integer(), nullable=False, unique=True, default=_next_sortkey,
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

    prompt = DB.relationship(
        'Prompt',
        primaryjoin='Mapper.prompt_prime == Prompt.prime',
        backref=DB.backref(
            'mapping',
            order_by='Mapper.sortkey.asc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        order_by='Prompt.created.desc()',
        lazy=True,
    )
    sensor = DB.relationship(
        'Sensor',
        primaryjoin='Mapper.sensor_prime == Sensor.prime',
        backref=DB.backref(
            'mapping',
            order_by='Mapper.sortkey.asc()',
            cascade='all,delete-orphan',
            lazy=True,
        ),
        order_by='Sensor.created.desc()',
        lazy=True,
    )

    @classmethod
    def by_commons(cls, prompt, sensor):
        return cls.query.filter(and_(
            cls.prompt == prompt,
            cls.sensor == sensor,
        )).first()

    @classmethod
    def query_sorted(cls, query=None):
        query = query if query is not None else cls.query
        return query.order_by(cls.sortkey.asc())

    def query_above(self, query=None):
        query = query if query is not None else self.query
        return self.query_sorted(query.filter(Mapper.sortkey > self.sortkey))

    def query_below(self, query=None):
        query = query if query is not None else self.query
        return self.query_sorted(query.filter(Mapper.sortkey < self.sortkey))

    def __flip_sortkey(self, that):
        skey = self.sortkey
        tkey = that.sortkey
        self.update(sortkey=_next_sortkey())
        that.update(sortkey=skey)
        self.update(sortkey=tkey)
        return True

    def raise_step(self):
        above = self.query_above().all()
        if not above:
            return False
        that, *_ = above
        return self.__flip_sortkey(that)

    def lower_step(self):
        below = self.query_below().all()
        if not below:
            return False
        *_, that = below
        return self.__flip_sortkey(that)
