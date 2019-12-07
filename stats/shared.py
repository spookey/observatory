from flask import render_template
from jinja2 import Markup

from stats.lib.text import random_line
from stats.start.environment import TAGLINES


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


def tagline():
    return Markup(random_line(TAGLINES))
