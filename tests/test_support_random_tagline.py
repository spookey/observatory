from stats.start.environment import (
    TAGLINE_01, TAGLINE_02, TAGLINE_03, TAGLINE_04, TAGLINE_05, TAGLINE_06
)
from stats.support import random_tagline


def test_random_tagline():
    pool = (
        TAGLINE_01, TAGLINE_02, TAGLINE_03,
        TAGLINE_04, TAGLINE_05, TAGLINE_06
    )
    for _ in range(42):
        assert random_tagline() in pool
