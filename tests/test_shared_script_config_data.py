from flask import url_for
from jinja2 import Markup

from observatory.shared import script_config_data
from observatory.start.environment import (
    FMT_MOMENT_DAY, FMT_MOMENT_DEFAULT, FMT_MOMENT_HOUR, FMT_MOMENT_MINUTE,
    FMT_MOMENT_MONTH, FMT_MOMENT_MSECOND, FMT_MOMENT_QUARTER,
    FMT_MOMENT_SECOND, FMT_MOMENT_WEEK, FMT_MOMENT_YEAR
)


def test_script_config_data():
    config = script_config_data()
    assert isinstance(config, Markup)

    plot_url = url_for('api.charts.plot', slug='', _external=True)
    text = config.unescape()

    assert f'data-api-plot-base="{plot_url}"' in text
    assert f'data-moment-default-format="{FMT_MOMENT_DEFAULT}"' in text
    assert f'data-moment-msecond-format="{FMT_MOMENT_MSECOND}"' in text
    assert f'data-moment-second-format="{FMT_MOMENT_SECOND}"' in text
    assert f'data-moment-minute-format="{FMT_MOMENT_MINUTE}"' in text
    assert f'data-moment-hour-format="{FMT_MOMENT_HOUR}"' in text
    assert f'data-moment-day-format="{FMT_MOMENT_DAY}"' in text
    assert f'data-moment-week-format="{FMT_MOMENT_WEEK}"' in text
    assert f'data-moment-month-format="{FMT_MOMENT_MONTH}"' in text
    assert f'data-moment-quarter-format="{FMT_MOMENT_QUARTER}"' in text
    assert f'data-moment-year-format="{FMT_MOMENT_YEAR}"' in text
