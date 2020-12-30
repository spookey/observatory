from flask import Blueprint, abort, current_app, render_template
from flask_login import login_required

BLUEPRINT_SAPI = Blueprint('sapi', __name__)


@BLUEPRINT_SAPI.route('/space')
@login_required
def index():
    if not current_app.config.get('SP_API_ENABLE', False):
        abort(404)

    return render_template(
        'sapi/index.html',
        title='Space API',
    )
