from flask import url_for
from jinja2 import Markup

from observatory.shared import script_config_data
from observatory.start.environment import FMT_MOMENT


def test_script_config_data():
    config = script_config_data()
    assert isinstance(config, Markup)

    plot_url = url_for('api.charts.plot', slug='', _external=True)
    text = config.unescape()

    assert f'data-api-plot-base="{plot_url}"' in text
    assert f'data-moment-default-format="{FMT_MOMENT}"' in text
