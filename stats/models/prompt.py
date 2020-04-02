from stats.database import CommonMixin, CreatedMixin, Model

# pylint: disable=too-many-ancestors


class Prompt(CommonMixin, CreatedMixin, Model):
    pass
