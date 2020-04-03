from random import choice
from urllib.parse import quote


def is_slugable(text):
    if (
            not isinstance(text, str) or
            not text or
            '/' in text
    ):
        return False

    return text == quote(text)


def random_line(lines, fallback=''):
    if not lines:
        return fallback

    lines = [line for line in lines if line and isinstance(line, str)]
    if not lines:
        return fallback

    return choice(lines)
