from observatory.database import CommonMixin, CreatedMixin, Model, SortMixin

# pylint: disable=too-many-ancestors


class Prompt(CommonMixin, SortMixin, CreatedMixin, Model):
    pass
