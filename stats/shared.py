from logging import getLogger

from flask import render_template
from jinja2 import Markup

from stats.lib.text import random_line
from stats.start.environment import TAGLINES

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
