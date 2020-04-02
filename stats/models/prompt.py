from stats.database import CommonMixin, CreatedMixin, Model
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Prompt(CommonMixin, CreatedMixin, Model):
    mapping = DB.relationship(
        'Mapper',
        primaryjoin='Prompt.prime == Mapper.prompt_prime',
        backref=DB.backref('prompt', lazy=True),
        order_by='Mapper.created.desc()',
        cascade='all,delete',
        lazy=True,
    )
