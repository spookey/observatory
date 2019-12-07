from random import choice
from urllib.parse import quote


def is_safename(text):
    if (
            not isinstance(text, str) or
            not text or
            '/' in text
    ):
        return False

    return text == quote(text)


def random_line(lines):
    if not lines:
        return ''

    lines = [line for line in lines if line and isinstance(line, str)]
    if not lines:
        return ''

    return choice(lines)
