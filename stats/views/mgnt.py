from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from stats.forms.common import PromptEditForm, SensorEditForm
from stats.models.prompt import Prompt
from stats.models.sensor import Sensor

BLUEPRINT_MGNT = Blueprint('mgnt', __name__)


@BLUEPRINT_MGNT.route('/manage/')
@BLUEPRINT_MGNT.route('/manage')
@login_required
def index():
    sensors = Sensor.query.all()
    prompts = Prompt.query.all()

    return render_template(
        'mgnt/index.html',
        title='Management',
        sensors=sensors,
        prompts=prompts,
    )


def _edit_common(form, slug=None):
    name = form.Model.__name__.lower()
    title = f'Edit {name}' if slug else f'Create new {name}'

    if request.method == 'POST' and form.validate_on_submit():
        thing = form.action()
        if thing is not None:
            flash(f'Saved {name} {thing.slug}!', 'success')
            return redirect(url_for('mgnt.index'))

    return render_template(
        'mgnt/edit_common.html',
        title=title,
        form=form,
    )


@BLUEPRINT_MGNT.route(
    '/manage/prompt/edit/<string:slug>',
    methods=['GET', 'POST']
)
@BLUEPRINT_MGNT.route(
    '/manage/prompt/edit/',
    methods=['GET', 'POST']
)
@BLUEPRINT_MGNT.route(
    '/manage/prompt/edit',
    methods=['GET', 'POST']
)
@login_required
def edit_prompt(slug=None):
    return _edit_common(
        PromptEditForm(obj=Prompt.by_slug(slug)),
    )


@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit/<string:slug>',
    methods=['GET', 'POST']
)
@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit/',
    methods=['GET', 'POST']
)
@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit',
    methods=['GET', 'POST']
)
@login_required
def edit_sensor(slug=None):
    return _edit_common(
        SensorEditForm(obj=Sensor.by_slug(slug)),
    )
