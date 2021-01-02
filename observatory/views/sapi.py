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

from observatory.forms.sp_api import (
    SpaceEditCamForm,
    SpaceEditContactForm,
    SpaceEditFeedBlogForm,
    SpaceEditFeedCalendarForm,
    SpaceEditFeedFlickrForm,
    SpaceEditFeedWikiForm,
    SpaceEditInfoForm,
    SpaceEditKeymastersForm,
    SpaceEditLinksForm,
    SpaceEditLocationForm,
    SpaceEditMembershipPlansForm,
    SpaceEditProjectsForm,
    SpaceEditSpaceFedForm,
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
        SpaceEditKeymastersForm(idx=idx), f'Keymaster #{ 1 + idx}'
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
