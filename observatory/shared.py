from logging import getLogger

from flask import render_template
from jinja2 import Markup

from observatory.lib.text import random_line
from observatory.start.environment import FMT_MOMENT, TAGLINES

LOG = getLogger(__name__)


def errorhandler(error):
    LOG.error(
        'handling error "%s" - "%s"',
        error.code, error.description
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
