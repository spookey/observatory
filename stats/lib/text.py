from urllib.parse import quote


def is_safename(text):
    if (
            not isinstance(text, str) or
            not text or
            '/' in text
    ):
        return False

    return text == quote(text)
