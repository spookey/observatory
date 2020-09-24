from logging import getLogger

from flask import render_template, request, url_for
from jinja2 import Markup

from observatory.forms.common import (
    PromptDropForm,
    PromptSortForm,
    SensorDropForm,
    SensorSortForm,
)
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.lib.text import random_line
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
    TAGLINES,
)

LOG = getLogger(__name__)


def errorhandler(error):
    LOG.error(
        'handling error "%s" - "%s" for "%s %s"',
        error.code,
        error.description,
        request.method,
        request.url,
    )

    return (
        render_template(
            'error.html',
            error=error,
            title=error.code,
        ),
        error.code,
    )


def tagline():
    return Markup(random_line(TAGLINES))


def script_config_data():
    api_plot_base_url = url_for('api.charts.plot', slug='', _external=True)

    return Markup(
        ' '.join(
            line.strip()
            for line in f'''
data-api-plot-base-url="{api_plot_base_url}"
data-api-plot-refresh-ms="{API_PLOT_REFRESH_MS}"
data-moment-default-format="{FMT_MOMENT_DEFAULT}"
data-moment-msecond-format="{FMT_MOMENT_MSECOND}"
data-moment-second-format="{FMT_MOMENT_SECOND}"
data-moment-minute-format="{FMT_MOMENT_MINUTE}"
data-moment-hour-format="{FMT_MOMENT_HOUR}"
data-moment-day-format="{FMT_MOMENT_DAY}"
data-moment-week-format="{FMT_MOMENT_WEEK}"
data-moment-month-format="{FMT_MOMENT_MONTH}"
data-moment-quarter-format="{FMT_MOMENT_QUARTER}"
data-moment-year-format="{FMT_MOMENT_YEAR}"
    '''.splitlines()
        ).strip()
    )


def form_drop_mapper(mapper):
    return MapperDropForm(obj=mapper)


def form_drop_prompt(prompt):
    return PromptDropForm(obj=prompt)


def form_drop_sensor(sensor):
    return SensorDropForm(obj=sensor)


def form_sort_mapper(mapper, lift):
    return MapperSortForm(obj=mapper, lift=lift)


def form_sort_prompt(prompt, lift):
    return PromptSortForm(obj=prompt, lift=lift)


def form_sort_sensor(sensor, lift):
    return SensorSortForm(obj=sensor, lift=lift)
