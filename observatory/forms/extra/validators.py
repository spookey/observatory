from wtforms import ValidationError

from observatory.lib.text import is_slugable

# pylint: disable=too-few-public-methods


class SafeSlug:
    def __init__(self, message=None):
        self.message = (
            message if message is not None else 'This is not a safe slug'
        )

    def __call__(self, _, field):
        if not is_slugable(field.data):
            raise ValidationError(self.message)


class NeedStart:
    def __init__(self, *symbols, message=None):
        self.symbols = symbols

        disp = '", "'.join(self.symbols)
        self.message = (
            message
            if message is not None
            else f'One of the prefixes "{disp}" is missing'
        )

    def __call__(self, _, field):
        if not any(field.data.startswith(char) for char in self.symbols):
            raise ValidationError(self.message)


class NeedInner:
    def __init__(self, chars, message=None, only=False):
        self.chars = chars
        self.only = only

        disp = '", "'.join(self.chars)
        self.message = (
            message
            if message is not None
            else (
                f'Only the symbols "{disp}" are permitted'
                if self.only
                else f'One of the symbols "{disp}" is missing'
            )
        )

    def __call__(self, _, field):
        func = all if self.only else any
        if not func(char in self.chars for char in field.data):
            raise ValidationError(self.message)
