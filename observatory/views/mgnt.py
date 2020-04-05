from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from observatory.forms.common import PromptEditForm, SensorEditForm
from observatory.forms.mapper import MapperEditForm
from observatory.models.mapper import Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor

BLUEPRINT_MGNT = Blueprint('mgnt', __name__)


@BLUEPRINT_MGNT.route('/manage')
@login_required
def index():
    return render_template(
        'mgnt/index.html',
        title='Management',
        mapping=Mapper.query.count(),
        prompts=Prompt.query.count(),
        sensors=Sensor.query.count(),
    )


@BLUEPRINT_MGNT.route('/manage/mapper/view')
@login_required
def view_mapper():
    return render_template(
        'mgnt/view.html',
        title='View mapping',
        mapping=Mapper.query_sorted().all(),
    )


@BLUEPRINT_MGNT.route('/manage/prompt/view')
@login_required
def view_prompt():
    return render_template(
        'mgnt/view.html',
        title='View prompts',
        prompts=Prompt.query_sorted().all(),
    )


@BLUEPRINT_MGNT.route('/manage/sensor/view')
@login_required
def view_sensor():
    return render_template(
        'mgnt/view.html',
        title='View sensors',
        sensors=Sensor.query_sorted().all(),
    )


@BLUEPRINT_MGNT.route(
    '/manage/mapper/edit'
    '/sensor/<string:sensor_slug>'
    '/prompt/<string:prompt_slug>',
    methods=['GET', 'POST'],
)
@BLUEPRINT_MGNT.route(
    '/manage/mapper/edit'
    '/prompt/<string:prompt_slug>'
    '/sensor/<string:sensor_slug>',
    methods=['GET', 'POST'],
)
@BLUEPRINT_MGNT.route(
    '/manage/mapper/edit',
    methods=['GET', 'POST'],
)
@login_required
def edit_mapper(prompt_slug=None, sensor_slug=None):
    title = 'Edit mapper' if (
        prompt_slug and sensor_slug
    ) else 'Create new mapper'
    form = MapperEditForm(obj=Mapper.by_commons(
        prompt=Prompt.by_slug(prompt_slug),
        sensor=Sensor.by_slug(sensor_slug),
    ))

    if request.method != 'POST':
        form.set_selections()
    if request.method == 'POST' and form.validate_on_submit():
        mapper = form.action()
        if mapper is not None:
            flash(
                f'Saved mapper {mapper.prompt.slug} {mapper.sensor.slug}!',
                'success'
            )
            return redirect(url_for('mgnt.view_mapper'))

    return render_template(
        'mgnt/edit.html',
        title=title,
        form=form,
    )


def _edit_common(form, redirect_ep):
    name = form.Model.__name__.lower()
    title = f'Edit {name}' if form.thing else f'Create new {name}'

    if request.method == 'POST' and form.validate_on_submit():
        thing = form.action()
        if thing is not None:
            flash(f'Saved {name} {thing.slug}!', 'success')
            return redirect(url_for(redirect_ep))

    return render_template(
        'mgnt/edit.html',
        title=title,
        form=form,
    )


@BLUEPRINT_MGNT.route(
    '/manage/prompt/edit/<string:slug>',
    methods=['GET', 'POST'],
)
@BLUEPRINT_MGNT.route(
    '/manage/prompt/edit',
    methods=['GET', 'POST'],
)
@login_required
def edit_prompt(slug=None):
    return _edit_common(
        PromptEditForm(obj=Prompt.by_slug(slug)),
        'mgnt.view_prompt',
    )


@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit/<string:slug>',
    methods=['GET', 'POST'],
)
@BLUEPRINT_MGNT.route(
    '/manage/sensor/edit',
    methods=['GET', 'POST'],
)
@login_required
def edit_sensor(slug=None):
    return _edit_common(
        SensorEditForm(obj=Sensor.by_slug(slug)),
        'mgnt.view_sensor',
    )
