from datetime import datetime
from logging import getLogger

from flask_login import UserMixin

from observatory.database import TXT_LEN_SHORT, CreatedMixin, Model
from observatory.lib.clock import (
    epoch_milliseconds,
    epoch_seconds,
    time_format,
)
from observatory.models.point import Point
from observatory.start.extensions import BCRYPT, DB

LOG = getLogger(__name__)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class User(UserMixin, CreatedMixin, Model):
    username = DB.Column(
        DB.String(length=TXT_LEN_SHORT), unique=True, nullable=False
    )
    pw_hash = DB.Column(DB.LargeBinary(length=TXT_LEN_SHORT), nullable=True)
    active = DB.Column(DB.Boolean(), nullable=False, default=True)
    last_login = DB.Column(DB.DateTime(), nullable=True)

    points = DB.relationship(
        'Point',
        backref=DB.backref('user', lazy=True),
        order_by='Point.created.desc()',
        cascade='all,delete-orphan',
        lazy=True,
    )

    def __init__(self, username, password, **kwargs):
        Model.__init__(self, username=username, **kwargs)
        self.set_password(password, _commit=False)

    @classmethod
    def by_username(cls, username):
        return cls.query.filter(cls.username == username).first()

    def get_id(self):
        '''required by flask-login'''
        return str(self.prime)

    @property
    def is_active(self):
        '''required by flask-login'''
        return self.active

    @property
    def last_login_fmt(self):
        return time_format(self.last_login)

    @property
    def last_login_epoch(self):
        return epoch_seconds(self.last_login)

    @property
    def last_login_epoch_ms(self):
        return epoch_milliseconds(self.last_login)

    def check_password(self, plain):
        if plain is None:
            return False
        return BCRYPT.check_password_hash(self.pw_hash, plain)

    @staticmethod
    def hash_password(plain):
        if plain is not None:
            return BCRYPT.generate_password_hash(plain)
        return None

    def set_password(self, plain, _commit=True):
        return self.update(pw_hash=self.hash_password(plain), _commit=_commit)

    def refresh(self, _commit=True):
        LOG.info('refreshing last_login for "%s"', self.username)

        return self.update(last_login=datetime.utcnow(), _commit=_commit)

    @property
    def query_points(self):
        return Point.query_sorted(query=Point.query.with_parent(self))

    @property
    def length(self):
        return self.query_points.count()

    @property
    def latest(self):
        return self.query_points.first()
