from jinja2 import Markup

from observatory.shared import tagline
from observatory.start.environment import TAGLINES


def test_tagline():
    for _ in range(23):
        line = tagline()
        assert isinstance(line, Markup)
        assert line.unescape() in TAGLINES
