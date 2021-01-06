from enum import Enum

from sqlalchemy import and_, asc
from sqlalchemy.ext.hybrid import hybrid_property

from observatory.database import Model
from observatory.start.extensions import DB


class EnumBox(Enum):
    STRING = '_string'
    NUMBER = '_number'
    SWITCH = '_switch'

    @classmethod
    def from_type(cls, val):
        if isinstance(val, bool):
            return cls.SWITCH
        if isinstance(val, (int, float)):
            return cls.NUMBER
        return cls.STRING


# pylint: disable=no-member


class Value(Model):
    key = DB.Column(
        DB.String(),
        nullable=False,
    )
    idx = DB.Column(
        DB.Integer(),
        nullable=False,
        default=0,
    )
    box = DB.Column(
        DB.Enum(EnumBox),
        nullable=False,
        default=EnumBox.STRING,
    )
    _string = DB.Column(
        DB.String(),
        nullable=True,
    )
    _number = DB.Column(
        DB.Float(),
        nullable=True,
    )
    _switch = DB.Column(
        DB.Boolean(),
        nullable=True,
    )

    sensor_prime = DB.Column(
        DB.Integer(),
        DB.ForeignKey('sensor.prime'),
        nullable=True,
    )

    @classmethod
    def by_key_idx(cls, key, idx=0):
        return cls.query.filter(
            and_(
                cls.key == key,
                cls.idx == idx,
            )
        ).first()

    @classmethod
    def by_key(cls, key):
        return (
            cls.query.filter(
                cls.key == key,
            )
            .order_by(asc(cls.idx))
            .all()
        )

    @hybrid_property
    def value(self):
        return getattr(self, self.box.value, None)

    @value.setter
    def value(self, val):
        box = EnumBox.from_type(val)
        self.update(
            box=box,
            **{bx.value: (None if bx != box else val) for bx in EnumBox},
        )

    @classmethod
    def get(cls, key, idx=0):
        obj = cls.by_key_idx(key, idx=idx)
        return obj.value if obj is not None else None

    @classmethod
    def get_all(cls, key):
        return [obj.value for obj in cls.by_key(key)]

    @classmethod
    def set(cls, key, idx=0, value=None):
        obj = cls.by_key_idx(key=key, idx=idx)
        if obj is None:
            obj = cls.create(key=key, idx=idx)
        return obj.update(value=value)
