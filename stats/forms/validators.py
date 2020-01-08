from wtforms import ValidationError

from stats.lib.text import is_safename

# pylint: disable=too-few-public-methods


class SafeName:
    def __init__(self, message=None):
        if message is None:
            message = 'This is not a safe name'
        self.message = message

    def __call__(self, _, field):
        if not is_safename(field.data):
            raise ValidationError(self.message)
