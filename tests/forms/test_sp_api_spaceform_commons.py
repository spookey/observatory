from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.sp_api import (
    SpaceCamForm,
    SpaceContactForm,
    SpaceFeedBlogForm,
    SpaceFeedCalendarForm,
    SpaceFeedFlickrForm,
    SpaceFeedWikiForm,
    SpaceInfoForm,
    SpaceKeymastersForm,
    SpaceLinksForm,
    SpaceLocationForm,
    SpaceMembershipPlansForm,
    SpaceProjectsForm,
    SpaceSpaceFedForm,
)
from observatory.logic.space_api import PREFIX
from observatory.models.values import Values


def form_meta(form, *, keys, data, any_of=None, **kwargs):
    def res():
        pass

    res.form = form
    res.data = data
    res.keys = keys
    res.any_of = any_of if any_of is not None else {}
    res.empty = kwargs.get('empty', False)

    return res


FORMS = [
    form_meta(
        SpaceInfoForm,
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
    form_meta(
        SpaceLocationForm,
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
    form_meta(
        SpaceSpaceFedForm,
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
    form_meta(
        SpaceCamForm,
        keys=dict(cam='cam'),
        data=dict(cam='https://example.org/webcam.mjpeg'),
    ),
    form_meta(
        SpaceContactForm,
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
        any_of=dict(
            email='E-Mail',
            issue_mail='Issue Mail',
            twitter='Twitter',
            mailinglist='Mailinglist',
        ),
    ),
    form_meta(
        SpaceKeymastersForm,
        keys=dict(
            name='contact.keymasters.name',
            irc_nick='contact.keymasters.irc_nick',
            phone='contact.keymasters.phone',
            email='contact.keymasters.email',
            twitter='contact.keymasters.twitter',
            xmpp='contact.keymasters.xmpp',
            matrix='contact.keymasters.matrix',
            mastodon='contact.keymasters.mastodon',
        ),
        data=dict(
            name='somebody',
            irc_nick='somebody',
            phone='+1 234 567 890',
            email='somebody@example.org',
            twitter='@somebody',
            xmpp='somebody@chat.example.org',
            matrix='@somebody@matrix.example.org',
            mastodon='@somebody@example.org',
        ),
        any_of=dict(
            irc_nick='IRC Nick',
            phone='Phone',
            email='E-Mail',
            twitter='Twitter',
        ),
    ),
    form_meta(
        SpaceFeedBlogForm,
        keys=dict(
            type_sel='feeds.blog.type',
            url='feeds.blog.url',
        ),
        data=dict(
            type_sel='atom',
            url='https://blog.example.org/feed',
        ),
    ),
    form_meta(
        SpaceFeedWikiForm,
        keys=dict(
            type_sel='feeds.wiki.type',
            url='feeds.wiki.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://wiki.example.org/feed.xml',
        ),
    ),
    form_meta(
        SpaceFeedCalendarForm,
        keys=dict(
            type_sel='feeds.calendar.type',
            url='feeds.calendar.url',
        ),
        data=dict(
            type_sel='ical',
            url='https://calendar.example.org/ical',
        ),
    ),
    form_meta(
        SpaceFeedFlickrForm,
        keys=dict(
            type_sel='feeds.flickr.type',
            url='feeds.flickr.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://example.com/space/feed.rss',
        ),
    ),
    form_meta(
        SpaceProjectsForm,
        keys=dict(projects='projects'),
        data=dict(projects='https://project.example.org/'),
    ),
    form_meta(
        SpaceLinksForm,
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
    form_meta(
        SpaceMembershipPlansForm,
        keys=dict(
            name='membership_plans.name',
            value='membership_plans.value',
            currency_sel='membership_plans.currency',
            billing_interval_sel='membership_plans.billing_interval',
            description='membership_plans.description',
        ),
        data=dict(
            name='some plan',
            value=23.5,
            currency_sel='RUB',
            billing_interval_sel='daily',
            description='please pay',
        ),
    ),
]
IDS = [meta.form.__name__ for meta in FORMS]


@mark.usefixtures('session', 'ctx_app')
class TestSpaceFormCommons:
    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_meta_meta(meta):
        keys = meta.keys.keys()
        assert sorted(keys) == sorted(meta.data.keys())
        for key in meta.any_of.keys():
            assert key in keys

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_meta_keys(meta):
        assert meta.form.KEYS == meta.keys

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_meta_any_of(meta):
        assert meta.form.ANY_OF == meta.any_of

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_basic_fields(meta):
        form = meta.form(idx=0)
        for field in meta.keys.keys():
            elem = getattr(form, field, 'error')
            assert elem is not None
            assert elem != 'error'
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_submit_button(meta):
        form = meta.form(idx=0)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_submit'

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_empty_invalid(meta):
        form = meta.form(idx=0)
        assert form.validate() is meta.empty
        action = form.action()
        if meta.empty:
            assert action is not None
        else:
            assert action is None

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_create_new(meta):
        assert Values.query.all() == []

        form = meta.form(idx=0, **meta.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in meta.keys.items():
            val = Values.get(key=f'{PREFIX}.{space_key}', idx=0)
            assert val is not None
            assert val == meta.data.get(form_key, 'error')

    @staticmethod
    @mark.parametrize('meta', FORMS, ids=IDS)
    def test_change_existing(meta):
        assert Values.query.all() == []

        for form_key, space_key in meta.keys.items():
            val = meta.data.get(form_key, 'some')
            if isinstance(val, bool):
                val = not val
            else:
                val = 2 * val

            Values.set(
                key=f'{PREFIX}.{space_key}',
                idx=0,
                value=val,
            )

        assert Values.query.all() != []

        form = meta.form(idx=0, **meta.data)
        assert form.validate() is True
        assert form.action()

        for form_key, space_key in meta.keys.items():
            val = Values.get(key=f'{PREFIX}.{space_key}', idx=0)
            assert val is not None
            assert val == meta.data.get(form_key, 'error')
