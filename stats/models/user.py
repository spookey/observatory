from datetime import datetime

from flask_login import UserMixin

from stats.database import Model
from stats.start.extensions import BCRYPT, DB

# pylint: disable=no-member


class User(UserMixin, Model):
    username = DB.Column(DB.String(length=128), unique=True, nullable=False)
    pw_hash = DB.Column(DB.LargeBinary(length=128), nullable=True)
    active = DB.Column(DB.Boolean(), nullable=False, default=True)
    last_login = DB.Column(DB.DateTime(), nullable=True)
    created = DB.Column(
        DB.DateTime(), nullable=False, default=datetime.utcnow
    )

    def __init__(self, username, password, **kwargs):
        Model.__init__(self, username=username, **kwargs)
        self.set_password(password)

    @classmethod
    def by_username(cls, username):
        return cls.query.filter(cls.username == username).first()

    def get_id(self):
        '''required by flask-login'''
        return str(self.prime)

    @property
    def is_active(self):
        return self.active

    def check_password(self, plain):
        if plain is None:
            return False
        return BCRYPT.check_password_hash(self.pw_hash, plain)

    @staticmethod
    def hash_password(plain):
        value = None
        if plain is not None:
            value = BCRYPT.generate_password_hash(plain)
        return value

    def set_password(self, plain):
        self.pw_hash = self.hash_password(plain)

    def set_last_login(self, _commit=True):
        self.last_login = datetime.utcnow()
        self.save(_commit=_commit)
