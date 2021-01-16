from datetime import datetime
from logging import getLogger

from sqlalchemy.ext.declarative import declared_attr

from observatory.lib.clock import (
    epoch_milliseconds,
    epoch_seconds,
    time_format,
)
from observatory.start.extensions import DB

LOG = getLogger(__name__)

TXT_LEN_SUPER = 4096
TXT_LEN_LARGE = 1024
TXT_LEN_SHORT = 256

# pylint: disable=comparison-with-callable
# pylint: disable=no-member
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-ancestors


class CRUDMixin:
    @classmethod
    def create(cls, _commit=True, **kwargs):
        LOG.info('creating model "%s"', cls.__name__)

        inst = cls(**kwargs)
        return inst.save(_commit=_commit)

    def update(self, _commit=True, **kwargs):
        LOG.info('updating model "%s"', self.__class__.__name__)

        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if _commit:
            return self.save(_commit=_commit)
        return self

    def save(self, _commit=True):
        LOG.info('saving model "%s"', self.__class__.__name__)

        DB.session.add(self)
        if _commit:
            DB.session.commit()
        return self

    def delete(self, _commit=True):
        LOG.info('deleting model "%s"', self.__class__.__name__)

        DB.session.delete(self)
        if _commit:
            DB.session.commit()
        return True


class NameMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class PrimeMixin:
    prime = DB.Column(DB.Integer(), primary_key=True)

    @classmethod
    def by_prime(cls, value):
        if any(
            [
                isinstance(value, (bytes, str)) and value.isdigit(),
                isinstance(value, (float, int)),
            ]
        ):
            return cls.query.get(int(value))
        return None


class CommonMixin:
    @declared_attr
    def slug(_):
        return DB.Column(
            DB.String(length=TXT_LEN_SHORT), unique=True, nullable=False
        )

    @declared_attr
    def title(_):
        return DB.Column(DB.String(length=TXT_LEN_LARGE), nullable=False)

    @declared_attr
    def description(_):
        return DB.Column(DB.String(length=TXT_LEN_SUPER), nullable=False)

    @classmethod
    def by_slug(cls, slug):
        return cls.query.filter(cls.slug == slug).first()


class CreatedMixin:
    @declared_attr
    def created(_):
        return DB.Column(
            DB.DateTime(), nullable=False, default=datetime.utcnow
        )

    @property
    def created_fmt(self):
        return time_format(self.created)

    @property
    def created_epoch(self):
        return epoch_seconds(self.created)

    @property
    def created_epoch_ms(self):
        return epoch_milliseconds(self.created)

    @classmethod
    def query_sorted(cls, *, query=None):
        query = query if query is not None else cls.query
        return query.order_by(cls.created.desc())


class SortMixin:
    @declared_attr
    def sortkey(cls):
        return DB.Column(
            DB.Integer(),
            nullable=False,
            unique=True,
            default=cls.sortkey_next,
        )

    @classmethod
    def sortkey_next(cls):
        return 1 + cls.query.count()

    @classmethod
    def _get_class_sortkey(cls):
        return cls.sortkey

    @classmethod
    def query_sorted(cls, *, query=None):
        query = query if query is not None else cls.query
        return query.order_by(cls._get_class_sortkey().desc())

    def query_above(self, *, query=None):
        query = query if query is not None else self.query
        return query.filter(self._get_class_sortkey() > self.sortkey)

    def query_below(self, *, query=None):
        query = query if query is not None else self.query
        return query.filter(self._get_class_sortkey() < self.sortkey)

    def __flip_sortkey(self, that):
        if not that:
            return None

        LOG.info(
            'flipping sortkey %d with %d for "%s"',
            self.sortkey,
            that.sortkey,
            self,
        )
        skey = self.sortkey
        tkey = that.sortkey
        self.update(sortkey=self.sortkey_next())
        that.update(sortkey=skey)
        self.update(sortkey=tkey)

        return that

    def raise_step(self):
        return self.__flip_sortkey(
            self.query_above(
                query=self.query.order_by(self._get_class_sortkey().asc())
            ).first()
        )

    def lower_step(self):
        return self.__flip_sortkey(
            self.query_below(
                query=self.query.order_by(self._get_class_sortkey().desc())
            ).first()
        )


class BaseModel(CRUDMixin, NameMixin, DB.Model):
    __abstract__ = True


class Model(PrimeMixin, BaseModel):
    __abstract__ = True
