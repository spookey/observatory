from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required

from observatory.forms.space_drop import (
    SpaceDropCamForm,
    SpaceDropContactKeymastersForm,
    SpaceDropLinksForm,
    SpaceDropMembershipPlansForm,
    SpaceDropProjectsForm,
    SpaceDropSensorsAccountBalanceForm,
    SpaceDropSensorsBarometerForm,
    SpaceDropSensorsBeverageSupplyForm,
    SpaceDropSensorsDoorLockedForm,
    SpaceDropSensorsHumidityForm,
    SpaceDropSensorsPowerConsumptionForm,
    SpaceDropSensorsTemperatureForm,
    SpaceDropSensorsTotalMemberCountForm,
)
from observatory.forms.space_edit import (
    SpaceEditCamForm,
    SpaceEditContactForm,
    SpaceEditContactKeymastersForm,
    SpaceEditFeedBlogForm,
    SpaceEditFeedCalendarForm,
    SpaceEditFeedFlickrForm,
    SpaceEditFeedWikiForm,
    SpaceEditInfoForm,
    SpaceEditLinksForm,
    SpaceEditLocationForm,
    SpaceEditMembershipPlansForm,
    SpaceEditProjectsForm,
    SpaceEditSensorsAccountBalanceForm,
    SpaceEditSensorsBarometerForm,
    SpaceEditSensorsBeverageSupplyForm,
    SpaceEditSensorsDoorLockedForm,
    SpaceEditSensorsHumidityForm,
    SpaceEditSensorsPowerConsumptionForm,
    SpaceEditSensorsTemperatureForm,
    SpaceEditSensorsTotalMemberCountForm,
    SpaceEditSpaceFedForm,
    SpaceEditStateIconForm,
)

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


def _edit_form(form, title):
    _enabled()

    if request.method == 'POST' and form.validate_on_submit():
        if form.action() is not None:
            flash(f'{title} saved!', 'success')
            return redirect(url_for('sapi.index'))

    return render_template(
        'page_form.html',
        title=title,
        form=form,
    )


@BLUEPRINT_SAPI.route('/space/edit/info', methods=['GET', 'POST'])
@login_required
def edit_info():
    return _edit_form(SpaceEditInfoForm(), 'Basic information')


@BLUEPRINT_SAPI.route('/space/edit/location', methods=['GET', 'POST'])
@login_required
def edit_location():
    return _edit_form(SpaceEditLocationForm(), 'Location')


@BLUEPRINT_SAPI.route('/space/edit/spacefed', methods=['GET', 'POST'])
@login_required
def edit_spacefed():
    return _edit_form(SpaceEditSpaceFedForm(), 'SpaceFED')


@BLUEPRINT_SAPI.route('/space/edit/cam/<int:idx>', methods=['GET', 'POST'])
@BLUEPRINT_SAPI.route('/space/edit/cam', methods=['GET', 'POST'])
@login_required
def edit_cam(idx=0):
    return _edit_form(SpaceEditCamForm(idx=idx), f'Webcam #{1 + idx}')


@BLUEPRINT_SAPI.route('/space/edit/state/icon', methods=['GET', 'POST'])
@login_required
def edit_state_icon():
    return _edit_form(SpaceEditStateIconForm(), 'State Icons')


@BLUEPRINT_SAPI.route('/space/edit/contact', methods=['GET', 'POST'])
@login_required
def edit_contact():
    return _edit_form(SpaceEditContactForm(), 'Contact')


@BLUEPRINT_SAPI.route(
    '/space/edit/contact/keymasters/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/contact/keymasters', methods=['GET', 'POST']
)
@login_required
def edit_contact_keymasters(idx=0):
    return _edit_form(
        SpaceEditContactKeymastersForm(idx=idx), f'Keymaster #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/temperature/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/temperature', methods=['GET', 'POST']
)
@login_required
def edit_sensors_temperature(idx=0):
    return _edit_form(
        SpaceEditSensorsTemperatureForm(idx=idx),
        f'Temperature sensor #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/door-locked/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/door-locked', methods=['GET', 'POST']
)
@login_required
def edit_sensors_door_locked(idx=0):
    return _edit_form(
        SpaceEditSensorsDoorLockedForm(idx=idx),
        f'Door locked sensor #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/barometer/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route('/space/edit/sensors/barometer', methods=['GET', 'POST'])
@login_required
def edit_sensors_barometer(idx=0):
    return _edit_form(
        SpaceEditSensorsBarometerForm(idx=idx), f'Barometer #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/humidity/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route('/space/edit/sensors/humidity', methods=['GET', 'POST'])
@login_required
def edit_sensors_humidity(idx=0):
    return _edit_form(
        SpaceEditSensorsHumidityForm(idx=idx), f'Humidity sensor #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/beverage-supply/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/beverage-supply', methods=['GET', 'POST']
)
@login_required
def edit_sensors_beverage_supply(idx=0):
    return _edit_form(
        SpaceEditSensorsBeverageSupplyForm(idx=idx),
        f'Beverage supply #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/power-consumption/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/power-consumption', methods=['GET', 'POST']
)
@login_required
def edit_sensors_power_consumption(idx=0):
    return _edit_form(
        SpaceEditSensorsPowerConsumptionForm(idx=idx),
        f'Power consumption #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/account-balance/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/account-balance', methods=['GET', 'POST']
)
@login_required
def edit_sensors_account_balance(idx=0):
    return _edit_form(
        SpaceEditSensorsAccountBalanceForm(idx=idx),
        f'Account balance #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/total-member-count/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route(
    '/space/edit/sensors/total-member-count', methods=['GET', 'POST']
)
@login_required
def edit_sensors_total_member_count(idx=0):
    return _edit_form(
        SpaceEditSensorsTotalMemberCountForm(idx=idx),
        f'Total member count #{1 + idx}',
    )


@BLUEPRINT_SAPI.route('/space/edit/feeds/blog', methods=['GET', 'POST'])
@login_required
def edit_feeds_blog():
    return _edit_form(SpaceEditFeedBlogForm(), 'Blog feed')


@BLUEPRINT_SAPI.route('/space/edit/feeds/wiki', methods=['GET', 'POST'])
@login_required
def edit_feeds_wiki():
    return _edit_form(SpaceEditFeedWikiForm(), 'Wiki feed')


@BLUEPRINT_SAPI.route('/space/edit/feeds/calendar', methods=['GET', 'POST'])
@login_required
def edit_feeds_calendar():
    return _edit_form(SpaceEditFeedCalendarForm(), 'Calendar feed')


@BLUEPRINT_SAPI.route('/space/edit/feeds/flickr', methods=['GET', 'POST'])
@login_required
def edit_feeds_flickr():
    return _edit_form(SpaceEditFeedFlickrForm(), 'Flickr feed')


@BLUEPRINT_SAPI.route(
    '/space/edit/projects/<int:idx>', methods=['GET', 'POST']
)
@BLUEPRINT_SAPI.route('/space/edit/projects', methods=['GET', 'POST'])
@login_required
def edit_projects(idx=0):
    return _edit_form(SpaceEditProjectsForm(idx=idx), f'Project #{1 + idx}')


@BLUEPRINT_SAPI.route('/space/edit/links/<int:idx>', methods=['GET', 'POST'])
@BLUEPRINT_SAPI.route('/space/edit/links', methods=['GET', 'POST'])
@login_required
def edit_links(idx=0):
    return _edit_form(SpaceEditLinksForm(idx=idx), f'Link #{1 + idx}')


@BLUEPRINT_SAPI.route('/space/edit/plans/<int:idx>', methods=['GET', 'POST'])
@BLUEPRINT_SAPI.route('/space/edit/plans', methods=['GET', 'POST'])
@login_required
def edit_membership_plans(idx=0):
    return _edit_form(
        SpaceEditMembershipPlansForm(idx=idx), f'Membership Plan #{1 + idx}'
    )


def _drop_form(form, title):
    _enabled()

    if request.method == 'POST' and form.validate_on_submit():
        if form.action() is not None:
            flash(f'{title} deleted!', 'success')

    return redirect(url_for('sapi.index'))


@BLUEPRINT_SAPI.route('/space/drop/cam/<int:idx>', methods=['POST'])
@login_required
def drop_cam(idx):
    return _drop_form(SpaceDropCamForm(idx=idx), f'Webcam #{1 + idx}')


@BLUEPRINT_SAPI.route(
    '/space/drop/contact/keymasters/<int:idx>', methods=['POST']
)
@login_required
def drop_contact_keymasters(idx):
    return _drop_form(
        SpaceDropContactKeymastersForm(idx=idx), f'Keymaster #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/temperature/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_temperature(idx):
    return _drop_form(
        SpaceDropSensorsTemperatureForm(idx=idx),
        f'Temperature sensor #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/door-locked/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_door_locked(idx):
    return _drop_form(
        SpaceDropSensorsDoorLockedForm(idx=idx),
        f'Door locked sensor #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/barometer/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_barometer(idx):
    return _drop_form(
        SpaceDropSensorsBarometerForm(idx=idx), f'Barometer #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/humidity/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_humidity(idx):
    return _drop_form(
        SpaceDropSensorsHumidityForm(idx=idx), f'Humidity sensor #{1 + idx}'
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/beverage-supply/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_beverage_supply(idx):
    return _drop_form(
        SpaceDropSensorsBeverageSupplyForm(idx=idx),
        f'Beverage supply #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/power-consumption/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_power_consumption(idx):
    return _drop_form(
        SpaceDropSensorsPowerConsumptionForm(idx=idx),
        f'Power consumption #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/account-balance/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_account_balance(idx):
    return _drop_form(
        SpaceDropSensorsAccountBalanceForm(idx=idx),
        f'Account balance #{1 + idx}',
    )


@BLUEPRINT_SAPI.route(
    '/space/drop/sensors/total-member-count/<int:idx>', methods=['POST']
)
@login_required
def drop_sensors_total_member_count(idx):
    return _drop_form(
        SpaceDropSensorsTotalMemberCountForm(idx=idx),
        f'Total member count #{1 + idx}',
    )


@BLUEPRINT_SAPI.route('/space/drop/projects/<int:idx>', methods=['POST'])
@login_required
def drop_projects(idx):
    return _drop_form(SpaceDropProjectsForm(idx=idx), f'Project #{1 + idx}')


@BLUEPRINT_SAPI.route('/space/drop/links/<int:idx>', methods=['POST'])
@login_required
def drop_links(idx):
    return _drop_form(SpaceDropLinksForm(idx=idx), f'Link #{1 + idx}')


@BLUEPRINT_SAPI.route('/space/drop/plans/<int:idx>', methods=['POST'])
@login_required
def drop_membership_plans(idx):
    return _drop_form(
        SpaceDropMembershipPlansForm(idx=idx), f'Membership Plan #{1 + idx}'
    )
