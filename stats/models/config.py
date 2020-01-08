from stats.database import CommonMixin, CreatedMixin, Model
from stats.models.display import Display
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Config(CommonMixin, CreatedMixin, Model):
    displays = DB.relationship(
        Display,
        backref=DB.backref('config', lazy=True),
        primaryjoin='Config.prime == Display.config_pime',
        lazy=True,
    )
