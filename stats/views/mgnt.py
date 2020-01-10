from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from stats.forms.sensor import SensorEditForm
from stats.models.sensor import Sensor

BLUEPRINT_MGNT = Blueprint('mgnt', __name__)


@BLUEPRINT_MGNT.route('/manage')
@login_required
def index():
    sensors = Sensor.query.all()

    return render_template(
        'mgnt/index.html',
        title='Management',
        sensors=sensors,
    )


@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit/<string:slug>',
    methods=['GET', 'POST']
)
@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit',
    methods=['GET', 'POST']
)
@login_required
def edit_sensor(slug=None):
    title = 'Edit Sensor' if slug else 'Create new Sensor'
    form = SensorEditForm(obj=Sensor.by_slug(slug))

    if request.method == 'POST' and form.validate_on_submit():
        sensor = form.action()
        if sensor is not None:
            flash(f'Saved {sensor.slug}!', 'success')
            return redirect(url_for('mgnt.index'))

    return render_template(
        'mgnt/edit_sensor.html',
        title=title,
        form=form,
    )
