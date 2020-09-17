from logging import DEBUG, getLogger, INFO

from observatory.start.environment import MDL_NAME
from observatory.start.logger import FORMATTER, initialize_logging, STREAM


def test_init_basic():
    log = getLogger(MDL_NAME)
    assert log.name == MDL_NAME

    initialize_logging('info')

    assert log.level == INFO


def test_init_level_fallback():
    log = getLogger(MDL_NAME)

    initialize_logging('🎁')

    assert log.level == DEBUG


def test_formatter():
    assert STREAM.formatter == FORMATTER
