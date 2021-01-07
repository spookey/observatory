from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.space_edit import (
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
    SpaceEditSensorsTemperatureForm,
    SpaceEditSpaceFedForm,
    SpaceEditStateIconForm,
)
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


def form_edit(form, *, keys, data, one_of=None, sensors=None, **kwargs):
    def res():
        pass

    res.form = form
    res.data = data
    res.keys = keys
    res.one_of = one_of if one_of is not None else []
    res.sensors = sensors if sensors is not None else []
    res.empty = kwargs.get('empty', False)

    return res


FORMS = [
    form_edit(
        SpaceEditInfoForm,
        keys=dict(
            space='space',
            logo='logo',
            url='url',
        ),
        data=dict(
            space='some space',
            logo='https://example.org/logo.png',
            url='https://example.org',
        ),
    ),
    form_edit(
        SpaceEditLocationForm,
        keys=dict(
            address='location.address',
            lat='location.lat',
            lon='location.lon',
            timezone_sel='location.timezone',
        ),
        data=dict(
            address='somewhere',
            lat=23.5,
            lon=13.37,
            timezone_sel='UTC',
        ),
    ),
    form_edit(
        SpaceEditSpaceFedForm,
        keys=dict(
            spacenet='spacefed.spacenet',
            spacesaml='spacefed.spacesaml',
        ),
        data=dict(
            spacenet=True,
            spacesaml=False,
        ),
        empty=True,
    ),
    form_edit(
        SpaceEditCamForm,
        keys=dict(cam='cam'),
        data=dict(cam='https://example.org/webcam.mjpeg'),
    ),
    form_edit(
        SpaceEditStateIconForm,
        keys=dict(
            opened='state.icon.open',
            closed='state.icon.closed',
        ),
        data=dict(
            opened='https://example.org/open.png',
            closed='https://example.org/closed.png',
        ),
    ),
    form_edit(
        SpaceEditContactForm,
        keys=dict(
            phone='contact.phone',
            sip='contact.sip',
            irc='contact.irc',
            twitter='contact.twitter',
            mastodon='contact.mastodon',
            facebook='contact.facebook',
            identica='contact.identica',
            foursquare='contact.foursquare',
            email='contact.email',
            mailinglist='contact.ml',
            xmpp='contact.xmpp',
            issue_mail='contact.issue_mail',
            gopher='contact.gopher',
            matrix='contact.matrix',
            mumble='contact.mumble',
        ),
        data=dict(
            phone='+1 234 567 890',
            sip='sip:space@sip.example.org',
            irc='irc://example.org/#space',
            twitter='@space',
            mastodon='@space@example.net',
            facebook='https://example.com/space',
            identica='space@example.org',
            foursquare='000000000000000000000000',
            email='space@example.org',
            mailinglist='list@example.org',
            xmpp='chat@conference.example.org',
            issue_mail='space@example.org',
            gopher='gopher://gopher.space.example.org',
            matrix='#chat:example.org',
            mumble='mumble://mumble.example.org/space?version=0.0.1',
        ),
        one_of=['email', 'issue_mail', 'twitter', 'mailinglist'],
    ),
    form_edit(
        SpaceEditKeymastersForm,
        keys=dict(
            name='contact.keymasters.name',
            irc_nick='contact.keymasters.irc_nick',
            phone='contact.keymasters.phone',
            email='contact.keymasters.email',
            twitter='contact.keymasters.twitter',
            xmpp='contact.keymasters.xmpp',
            mastodon='contact.keymasters.mastodon',
            matrix='contact.keymasters.matrix',
        ),
        data=dict(
            name='somebody',
            irc_nick='somebody',
            phone='+1 234 567 890',
            email='somebody@example.org',
            twitter='@somebody',
            xmpp='somebody@chat.example.org',
            mastodon='@somebody@example.org',
            matrix='@somebody:matrix.example.org',
        ),
        one_of=[
            'irc_nick',
            'phone',
            'email',
            'twitter',
        ],
    ),
    form_edit(
        SpaceEditSensorsTemperatureForm,
        keys=dict(
            sensor_sel='sensors.temperature.value',
            elevate_sel='sensors.temperature.value.elevate',
            convert_sel='sensors.temperature.value.convert',
            horizon_sel='sensors.temperature.value.horizon',
            unit_sel='sensors.temperature.unit',
            location='sensors.temperature.location',
            name='sensors.temperature.name',
            description='sensors.temperature.description',
        ),
        data=dict(
            sensor_sel=2,
            elevate_sel=1.01,
            convert_sel=1,
            horizon_sel=2,
            unit_sel='°C',
            location='somewhere',
            name='temperature sensor',
            description='measures the temperature',
        ),
        sensors=['sensor_sel'],
    ),
    form_edit(
        SpaceEditFeedBlogForm,
        keys=dict(
            type_sel='feeds.blog.type',
            url='feeds.blog.url',
        ),
        data=dict(
            type_sel='atom',
            url='https://blog.example.org/feed',
        ),
    ),
    form_edit(
        SpaceEditFeedWikiForm,
        keys=dict(
            type_sel='feeds.wiki.type',
            url='feeds.wiki.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://wiki.example.org/feed.xml',
        ),
    ),
    form_edit(
        SpaceEditFeedCalendarForm,
        keys=dict(
            type_sel='feeds.calendar.type',
            url='feeds.calendar.url',
        ),
        data=dict(
            type_sel='ical',
            url='https://calendar.example.org/ical',
        ),
    ),
    form_edit(
        SpaceEditFeedFlickrForm,
        keys=dict(
            type_sel='feeds.flickr.type',
            url='feeds.flickr.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://example.com/space/feed.rss',
        ),
    ),
    form_edit(
        SpaceEditProjectsForm,
        keys=dict(projects='projects'),
        data=dict(projects='https://project.example.org/'),
    ),
    form_edit(
        SpaceEditLinksForm,
        keys=dict(
            name='links.name',
            description='links.description',
            url='links.url',
        ),
        data=dict(
            name='some link',
            description='This is just a link',
            url='https://example.org',
        ),
    ),
    form_edit(
        SpaceEditMembershipPlansForm,
        keys=dict(
            name='membership_plans.name',
            value='membership_plans.value',
            currency_sel='membership_plans.currency',
            billing_interval_sel='membership_plans.billing_interval',
            description='membership_plans.description',
        ),
        data=dict(
            name='gold plan',
            value=23.5,
            currency_sel='XAU',
            billing_interval_sel='hourly',
            description='please pay',
        ),
    ),
]
IDS = [edit.form.__name__ for edit in FORMS]


@mark.usefixtures('session', 'ctx_app')
class TestSpaceEditCommons:
    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_meta(edit):
        keys = edit.keys.keys()
        assert sorted(keys) == sorted(edit.data.keys())
        for key in edit.one_of:
            assert key in keys

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_keys(edit):
        assert edit.form.KEYS == edit.keys

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_edit_one_of(edit):
        assert edit.form.ONE_OF == edit.one_of

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_form_idx(edit):
        idx = choice(range(23, 42))
        form = edit.form(idx=idx)
        assert form.idx == idx

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_basic_fields(edit):
        form = edit.form(idx=0)
        for field in edit.keys.keys():
            elem = getattr(form, field, 'error')
            assert elem is not None
            assert elem != 'error'
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_submit_button(edit):
        form = edit.form(idx=0)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_submit'

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_empty_invalid(edit):
        form = edit.form(idx=0)
        assert form.validate() is edit.empty
        action = form.action()
        if edit.empty:
            assert action is not None
        else:
            assert action is None

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_create_new(edit, gen_sensor):
        assert Value.query.all() == []

        sensors = [
            gen_sensor(name, prime=edit.data[name]) for name in edit.sensors
        ]

        form = edit.form(idx=0, **edit.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in edit.keys.items():
            val = Value.by_key_idx(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            if form_key in edit.sensors:
                assert val.elem in sensors
            else:
                assert val.elem == edit.data.get(form_key, 'error')

    @staticmethod
    @mark.parametrize('edit', FORMS, ids=IDS)
    def test_change_existing(edit, gen_sensor):
        assert Value.query.all() == []

        sensors = [
            gen_sensor(name, prime=edit.data[name]) for name in edit.sensors
        ]

        for form_key, space_key in edit.keys.items():
            old_value = edit.data.get(form_key, 'some')

            if isinstance(old_value, bool):
                old_value = not old_value
            else:
                old_value = 2 * old_value

            if form_key in edit.sensors:
                old_value = gen_sensor(f'old_{form_key}', prime=old_value)

            Value.set(
                key=f'{SP_API_PREFIX}.{space_key}', idx=0, elem=old_value
            )

        assert Value.query.all() != []

        form = edit.form(idx=0, **edit.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in edit.keys.items():
            val = Value.by_key_idx(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            if form_key in edit.sensors:
                assert val.elem in sensors
            else:
                assert val.elem == edit.data.get(form_key, 'error')
