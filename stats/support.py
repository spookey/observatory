from random import choice

from stats.start.environment import (
    TAGLINE_01, TAGLINE_02, TAGLINE_03, TAGLINE_04, TAGLINE_05, TAGLINE_06
)


def random_tagline():
    return choice([line for line in (
        TAGLINE_01, TAGLINE_02, TAGLINE_03,
        TAGLINE_04, TAGLINE_05, TAGLINE_06,
    ) if line])
