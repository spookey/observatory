from flask import Blueprint, render_template

from stats.shared import tagline

BLUEPRINT_MAIN = Blueprint('main', __name__)


@BLUEPRINT_MAIN.route('/')
def index():
    return render_template(
        'main/index.html',
        title=tagline(),
    )
