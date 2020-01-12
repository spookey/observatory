from wtforms import ValidationError

from stats.lib.text import is_slugable

# pylint: disable=too-few-public-methods


class SafeSlug:
    def __init__(self, message=None):
        if message is None:
            message = 'This is not a safe slug'
        self.message = message

    def __call__(self, _, field):
        if not is_slugable(field.data):
            raise ValidationError(self.message)
