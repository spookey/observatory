from flask import current_app, url_for
from jinja2 import Markup
from pytest import mark

from observatory.shared import script_config_data
from observatory.start.environment import (
    API_PLOT_REFRESH_MS,
    FMT_MOMENT_DAY,
    FMT_MOMENT_DEFAULT,
    FMT_MOMENT_HOUR,
    FMT_MOMENT_MINUTE,
    FMT_MOMENT_MONTH,
    FMT_MOMENT_MSECOND,
    FMT_MOMENT_QUARTER,
    FMT_MOMENT_SECOND,
    FMT_MOMENT_WEEK,
    FMT_MOMENT_YEAR,
)


@mark.usefixtures('ctx_app')
@mark.parametrize('enabled', (True, False))
def test_script_config_data(enabled, monkeypatch):
    api_plot_base_url = url_for('api.charts.plot', slug='', _external=True)
    api_space_api_url = url_for('api.sp_api.json', _external=True)
    if not enabled:
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)
        api_space_api_url = ''

    config = script_config_data()
    assert isinstance(config, Markup)

    text = config.unescape()

    for line in (elem.strip() for elem in text.split('data') if elem.strip()):
        assert '="' in line
        assert line.endswith('"')

    assert f'data-api-plot-base-url="{api_plot_base_url}"' in text
    assert f'data-api-plot-refresh-ms="{API_PLOT_REFRESH_MS}"' in text
    assert f'data-api-space-api-url="{api_space_api_url}"' in text
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
