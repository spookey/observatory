from enum import Enum

from sqlalchemy import and_, asc
from sqlalchemy.ext.hybrid import hybrid_property

from observatory.database import TXT_LEN_SHORT, TXT_LEN_SUPER, Model
from observatory.models.sensor import Sensor
from observatory.start.extensions import DB


class EnumBox(Enum):
    STRING = '_string'
    NUMBER = '_number'
    SWITCH = '_switch'
    SENSOR = '_sensor'

    @classmethod
    def from_type(cls, val):
        if isinstance(val, Sensor):
            return cls.SENSOR
        if isinstance(val, bool):
            return cls.SWITCH
        if isinstance(val, (int, float)):
            return cls.NUMBER
        return cls.STRING


# pylint: disable=no-member


class Value(Model):
    key = DB.Column(
        DB.String(length=TXT_LEN_SHORT),
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
        DB.String(length=TXT_LEN_SUPER),
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
    _sensor = DB.Column(
        DB.Integer(),
        DB.ForeignKey('sensor.prime'),
        nullable=True,
    )

    @classmethod
    def by_key_idx(cls, *, key, idx=0):
        return cls.query.filter(
            and_(
                cls.key == key,
                cls.idx == idx,
            )
        ).first()

    @classmethod
    def by_key(cls, *, key):
        return (
            cls.query.filter(
                cls.key == key,
            )
            .order_by(asc(cls.idx))
            .all()
        )

    @hybrid_property
    def elem(self):
        if self.box == EnumBox.SENSOR:
            return self.sensor
        return getattr(self, self.box.value, None)

    @elem.setter
    def elem(self, val):
        box = EnumBox.from_type(val)
        underscore = {bx.value: None for bx in EnumBox}
        sensor = val
        if box != EnumBox.SENSOR:
            underscore.update({box.value: val})
            sensor = None
        self.update(box=box, sensor=sensor, **underscore)

    @classmethod
    def get(cls, *, key, idx=0):
        obj = cls.by_key_idx(key=key, idx=idx)
        return obj.elem if obj is not None else None

    @classmethod
    def get_all(cls, *, key):
        return [obj.elem for obj in cls.by_key(key=key)]

    @classmethod
    def set(cls, *, key, idx=0, elem=None, _commit=True):
        obj = cls.by_key_idx(key=key, idx=idx)
        if obj is None:
            obj = cls.create(key=key, idx=idx, _commit=False)
        return obj.update(elem=elem, _commit=_commit)

    @property
    def latest(self):
        if self.sensor is not None:
            return self.sensor.latest
        return None
