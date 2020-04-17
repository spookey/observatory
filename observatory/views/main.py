from flask import Blueprint, render_template

from observatory.models.prompt import Prompt
from observatory.shared import tagline

BLUEPRINT_MAIN = Blueprint('main', __name__)


@BLUEPRINT_MAIN.route('/')
def index():
    return render_template(
        'main/index.html',
        title=tagline(),
        prompts=Prompt.query_sorted().all(),
    )
