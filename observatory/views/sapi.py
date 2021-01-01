from flask import Blueprint, abort, current_app, render_template
from flask_login import login_required

BLUEPRINT_SAPI = Blueprint('sapi', __name__)


def _enabled():
    if not current_app.config.get('SP_API_ENABLE', False):
        abort(404)


@BLUEPRINT_SAPI.route('/space')
@login_required
def index():
    _enabled()

    return render_template(
        'sapi/index.html',
        title='Space API',
    )
