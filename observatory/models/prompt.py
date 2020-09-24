from observatory.database import CommonMixin, CreatedMixin, Model, SortMixin

# pylint: disable=too-many-ancestors


class Prompt(CommonMixin, SortMixin, CreatedMixin, Model):
    @property
    def active(self):
        return any(self.mapping_active)
