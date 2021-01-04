from flask import current_app, url_for
from pytest import mark

from observatory.models.values import Values
from observatory.start.environment import SP_API_PREFIX


def page_data(endpoint, *, url, keys, data, **kwargs):
    def res():
        pass

    res.endpoint = endpoint
    res.url = url
    res.keys = keys
    res.data = data
    res.multi = kwargs.get('multi', False)

    return res


PAGES = [
    page_data(
        'sapi.edit_info',
        url='/space/edit/info',
        keys=dict(
            space='space',
            logo='logo',
            url='url',
        ),
        data=dict(
            space='space',
            logo='https://example.org/logo.png',
            url='https://example.org',
        ),
    ),
    page_data(
        'sapi.edit_location',
        url='/space/edit/location',
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
    page_data(
        'sapi.edit_spacefed',
        url='/space/edit/spacefed',
        keys=dict(
            spacenet='spacefed.spacenet',
            spacesaml='spacefed.spacesaml',
        ),
        data=dict(
            spacenet=True,
            spacesaml=True,
        ),
    ),
    page_data(
        'sapi.edit_cam',
        url='/space/edit/cam',
        keys=dict(cam='cam'),
        data=dict(cam='https://example.org/webcam'),
        multi=True,
    ),
    page_data(
        'sapi.edit_contact',
        url='/space/edit/contact',
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
    ),
    page_data(
        'sapi.edit_contact_keymasters',
        url='/space/edit/contact/keymasters',
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
        multi=True,
    ),
    page_data(
        'sapi.edit_feeds_blog',
        url='/space/edit/feeds/blog',
        keys=dict(
            type_sel='feeds.blog.type',
            url='feeds.blog.url',
        ),
        data=dict(
            type_sel='atom',
            url='https://blog.example.org/feed',
        ),
    ),
    page_data(
        'sapi.edit_feeds_wiki',
        url='/space/edit/feeds/wiki',
        keys=dict(
            type_sel='feeds.wiki.type',
            url='feeds.wiki.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://wiki.example.org/feed.xml',
        ),
    ),
    page_data(
        'sapi.edit_feeds_calendar',
        url='/space/edit/feeds/calendar',
        keys=dict(
            type_sel='feeds.calendar.type',
            url='feeds.calendar.url',
        ),
        data=dict(
            type_sel='ical',
            url='https://calendar.example.org/ical',
        ),
    ),
    page_data(
        'sapi.edit_feeds_flickr',
        url='/space/edit/feeds/flickr',
        keys=dict(
            type_sel='feeds.flickr.type',
            url='feeds.flickr.url',
        ),
        data=dict(
            type_sel='rss',
            url='https://example.com/space/feed.rss',
        ),
    ),
    page_data(
        'sapi.edit_projects',
        url='/space/edit/projects',
        keys=dict(projects='projects'),
        data=dict(projects='https://project.example.org/'),
        multi=True,
    ),
    page_data(
        'sapi.edit_links',
        url='/space/edit/links',
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
        multi=True,
    ),
    page_data(
        'sapi.edit_membership_plans',
        url='/space/edit/plans',
        keys=dict(
            name='membership_plans.name',
            value='membership_plans.value',
            currency_sel='membership_plans.currency',
            billing_interval_sel='membership_plans.billing_interval',
            description='membership_plans.description',
        ),
        data=dict(
            name='silver plan',
            value=42.0,
            currency_sel='XAG',
            billing_interval_sel='hourly',
            description='please pay',
        ),
        multi=True,
    ),
]
IDS = [page.endpoint.split('.')[-1] for page in PAGES]


@mark.usefixtures('session')
class TestSapiEditCommons:
    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_page_page(page):
        assert sorted(page.keys.keys()) == sorted(page.data.keys())

    @staticmethod
    @mark.usefixtures('ctx_app')
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_urls(page):
        assert url_for(page.endpoint) == page.url
        if page.multi:
            assert url_for(page.endpoint, idx=23) == f'{page.url}/23'

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_no_user(page, visitor):
        visitor(page.endpoint, code=401)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_disabled(page, monkeypatch, visitor, gen_user_loggedin):
        gen_user_loggedin()
        monkeypatch.setitem(current_app.config, 'SP_API_ENABLE', False)

        visitor(page.endpoint, code=404)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_params(page, visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(page.endpoint)

        form = res.soup.select('form')[-1]
        assert form['method'] == 'POST'
        assert form['action'] == url_for(page.endpoint, _external=True)

    @staticmethod
    @mark.parametrize('page', PAGES, ids=IDS)
    def test_creates(page, visitor, gen_user_loggedin):
        gen_user_loggedin()
        index_url = url_for('sapi.index', _external=True)

        assert Values.query.all() == []

        res = visitor(
            page.endpoint,
            method='post',
            data={**page.data, 'submit': True},
            code=302,
        )

        assert res.request.headers['LOCATION'] == index_url
        for form_key, space_key in page.keys.items():
            val = Values.get(key=f'{SP_API_PREFIX}.{space_key}', idx=0)
            assert val is not None
            assert val == page.data.get(form_key, 'error')
