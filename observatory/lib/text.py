from random import choice
from urllib.parse import quote


def random_line(lines, fallback=''):
    if not lines:
        return fallback

    lines = [line for line in lines if line and isinstance(line, str)]
    if not lines:
        return fallback

    return choice(lines)


def is_slugable(text):
    if (
            not isinstance(text, str) or
            not text or
            '/' in text
    ):
        return False

    return text == quote(text)


def extract_slug(generic):
    result = [getattr(generic, 'slug', None)]
    if not any(result):
        for field in ('prompt', 'sensor'):
            thing = getattr(generic, field, None)
            if thing is not None:
                result.append(getattr(thing, 'slug', None))

    return ' '.join(sl for sl in result if sl is not None).strip()
