from jinja2 import Markup

from stats.shared import moment_config
from stats.start.environment import FMT_MOMENT


def test_moment_config():
    config = moment_config()
    assert isinstance(config, Markup)

    text = config.unescape()
    assert '<script>' in text
    assert '</script>' in text
    assert 'document.addEventListener' in text
    assert 'DOMContentLoaded' in text
    assert 'window.momentConfig' in text
    assert FMT_MOMENT in text
