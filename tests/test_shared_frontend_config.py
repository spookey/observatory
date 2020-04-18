from flask import url_for
from jinja2 import Markup

from observatory.shared import frontend_config
from observatory.start.environment import FMT_MOMENT


def test_frontend_config():
    config = frontend_config()
    assert isinstance(config, Markup)

    plot_url = url_for('api.charts.plot', slug='', _external=True)
    text = config.unescape()

    assert '<script>' in text
    assert '</script>' in text
    assert 'document.addEventListener' in text
    assert 'DOMContentLoaded' in text
    assert 'window.configure' in text
    assert f'"{FMT_MOMENT}"' in text
    assert f'"{plot_url}"' in text
