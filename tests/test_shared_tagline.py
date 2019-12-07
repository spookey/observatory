from jinja2 import Markup

from stats.shared import tagline
from stats.start.environment import (
    TAGLINE_01, TAGLINE_02, TAGLINE_03, TAGLINE_04, TAGLINE_05, TAGLINE_06
)


def test_random_tagline():
    pool = (
        TAGLINE_01, TAGLINE_02, TAGLINE_03,
        TAGLINE_04, TAGLINE_05, TAGLINE_06
    )
    for _ in range(23):
        line = tagline()
        assert isinstance(line, Markup)
        assert str(line) in pool
