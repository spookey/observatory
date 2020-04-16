from jinja2 import Markup

from observatory.shared import frontend_config
from observatory.start.environment import FMT_MOMENT


def test_frontend_config():
    config = frontend_config()
    assert isinstance(config, Markup)

    text = config.unescape()
    assert '<script>' in text
    assert '</script>' in text
    assert 'document.addEventListener' in text
    assert 'DOMContentLoaded' in text
    assert 'window.configure' in text
    assert f'"{FMT_MOMENT}"' in text
