from enum import Enum
from logging import getLogger

from sqlalchemy import and_

from observatory.database import BaseModel, CreatedMixin
from observatory.lib.text import extract_slug
from observatory.start.extensions import DB

LOG = getLogger(__name__)


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
        order_by='Prompt.created.desc()',
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
        return query.order_by(cls.sortkey.desc())

    def query_above(self, query=None):
        query = query if query is not None else self.query
        return query.filter(Mapper.sortkey > self.sortkey)

    def query_below(self, query=None):
        query = query if query is not None else self.query
        return query.filter(Mapper.sortkey < self.sortkey)

    def __flip_sortkey(self, that):
        if not that:
            return False
        LOG.info(
            'flipping sortkey from "%s" (%d) with "%s" (%d)',
            extract_slug(self), self.sortkey,
            extract_slug(that), that.sortkey,
        )

        skey = self.sortkey
        tkey = that.sortkey
        self.update(sortkey=_next_sortkey())
        that.update(sortkey=skey)
        self.update(sortkey=tkey)
        return True

    def raise_step(self):
        return self.__flip_sortkey(self.query_above(
            Mapper.query.order_by(Mapper.sortkey.asc())
        ).first())

    def lower_step(self):
        return self.__flip_sortkey(self.query_below(
            Mapper.query.order_by(Mapper.sortkey.desc())
        ).first())
