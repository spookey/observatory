from logging import getLogger

from flask import render_template, request
from jinja2 import Markup

from observatory.forms.common import (
    PromptDropForm, PromptSortForm, SensorDropForm, SensorSortForm
)
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.lib.text import random_line
from observatory.start.environment import FMT_MOMENT, TAGLINES

LOG = getLogger(__name__)


def errorhandler(error):
    LOG.error(
        'handling error "%s" - "%s" for "%s %s"',
        error.code, error.description, request.method, request.url
    )

    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


def tagline():
    return Markup(random_line(TAGLINES))


def moment_config():
    script = f'''
<script>
  document.addEventListener("DOMContentLoaded", function() {{
    window.momentConfig("{FMT_MOMENT}");
  }});
</script>
    '''
    return Markup(''.join(line.strip() for line in script.splitlines()))


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
