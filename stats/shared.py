from flask import render_template
from jinja2 import Markup

from stats.support import random_tagline


def errorhandler(error):
    return render_template(
        'error.html',
        error=error,
        title=error.code,
    ), error.code


def tagline():
    return Markup(random_tagline())
