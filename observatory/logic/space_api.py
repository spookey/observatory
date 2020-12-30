from datetime import datetime
from logging import getLogger

from observatory.models.values import Values
from observatory.start.environment import SP_API_REFRESH


class SpaceApi:
    def __init__(self):
        self._log = getLogger(self.__class__.__name__)
        self._content = None
        self._last = None

    @staticmethod
    def _contact_keymasters():
        '''One of irc_nick, phone, email or twitter must be specified'''
        indices = (
            set(
                elem.idx
                for elem in Values.by_key('contact.keymasters.irc_nick')
            )
            .union(
                elem.idx for elem in Values.by_key('contact.keymasters.phone')
            )
            .union(
                elem.idx for elem in Values.by_key('contact.keymasters.email')
            )
            .union(
                elem.idx
                for elem in Values.by_key('contact.keymasters.twitter')
            )
        )
        return [
            {
                'name': Values.get(key='contact.keymasters.name', idx=idx),
                'irc_nick': Values.get(
                    key='contact.keymasters.irc_nick', idx=idx
                ),
                'phone': Values.get(key='contact.keymasters.phone', idx=idx),
                'email': Values.get(key='contact.keymasters.email', idx=idx),
                'twitter': Values.get(
                    key='contact.keymasters.twitter', idx=idx
                ),
                'xmpp': Values.get(key='contact.keymasters.xmpp', idx=idx),
                'matrix': Values.get(key='contact.keymasters.matrix', idx=idx),
                'mastodon': Values.get(
                    key='contact.keymasters.mastodon', idx=idx
                ),
            }
            for idx in sorted(indices)
        ]

    @staticmethod
    def _links():
        indices = set(
            elem.idx for elem in Values.by_key('links.name')
        ).intersection(elem.idx for elem in Values.by_key('links.url'))
        return [
            {
                'name': Values.get(key='links.name', idx=idx),
                'description': Values.get(key='links.description', idx=idx),
                'url': Values.get(key='links.url', idx=idx),
            }
            for idx in sorted(indices)
        ]

    @staticmethod
    def _membership_plans():
        indices = (
            set(elem.idx for elem in Values.by_key('membership_plans.name'))
            .intersection(
                elem.idx for elem in Values.by_key('membership_plans.value')
            )
            .intersection(
                elem.idx for elem in Values.by_key('membership_plans.currency')
            )
            .intersection(
                elem.idx
                for elem in Values.by_key('membership_plans.billing_interval')
            )
        )
        return [
            {
                'name': Values.get(key='membership_plans.name', idx=idx),
                'value': Values.get(key='membership_plans.value', idx=idx),
                'currency': Values.get(
                    key='membership_plans.currency', idx=idx
                ),
                'billing_interval': Values.get(
                    key='membership_plans.billing_interval', idx=idx
                ),
                'description': Values.get(
                    key='membership_plans.description', idx=idx
                ),
            }
            for idx in sorted(indices)
        ]

    def build(self):
        return {
            'api_compatibility': ['14'],
            'space': Values.get('space'),
            'logo': Values.get('logo'),
            'url': Values.get('url'),
            'location': {
                'address': Values.get('location.address'),
                'lat': Values.get('location.lat'),
                'lon': Values.get('location.lon'),
                'timezone': Values.get('location.timezone'),
            },
            'spacefed': {
                'spacenet': Values.get('spacefed.spacenet'),
                'spacesaml': Values.get('spacefed.spacesaml'),
            },
            'cam': Values.get_all('cam'),
            'state': {},
            'events': [],
            'contact': {
                'phone': Values.get('contact.phone'),
                'sip': Values.get('contact.sip'),
                'keymasters': self._contact_keymasters(),
                'irc': Values.get('contact.irc'),
                'twitter': Values.get('contact.twitter'),
                'mastodon': Values.get('contact.mastodon'),
                'facebook': Values.get('contact.facebook'),
                'identica': Values.get('contact.identica'),
                'foursquare': Values.get('contact.foursquare'),
                'email': Values.get('contact.email'),
                'ml': Values.get('contact.ml'),
                'xmpp': Values.get('contact.xmpp'),
                'issue_mail': Values.get('contact.issue_mail'),
                'gopher': Values.get('contact.gopher'),
                'matrix': Values.get('contact.matrix'),
                'mumble': Values.get('contact.mumble'),
            },
            'sensors': {
                'temperature': [],
                'door_locked': [],
                'barometer': [],
                'radiation': [],
                'humidity': [],
                'beverage_supply': [],
                'power_consumption': [],
                'wind': [],
                'network_connections': [],
                'account_balance': [],
                'total_member_count': [],
                'people_now_present': [],
                'network_traffic': [],
            },
            'feeds': {
                'blog': {
                    'type': Values.get('feeds.blog.type'),
                    'url': Values.get('feeds.blog.url'),
                },
                'wiki': {
                    'type': Values.get('feeds.wiki.type'),
                    'url': Values.get('feeds.wiki.url'),
                },
                'calendar': {
                    'type': Values.get('feeds.calendar.type'),
                    'url': Values.get('feeds.calendar.url'),
                },
                'flickr': {
                    'type': Values.get('feeds.calendar.type'),
                    'url': Values.get('feeds.calendar.url'),
                },
            },
            'projects': Values.get_all('projects'),
            'links': self._links(),
            'membership_plans': self._membership_plans(),
        }

    def get_state(self):
        self._log.info('gathering state')
        return {}

    def get_events(self):
        self._log.info('gathering events')
        return []

    @property
    def outdated(self):
        if self._content is None:
            return True
        if self._last is None:
            return True
        if (datetime.utcnow() - self._last).total_seconds() > SP_API_REFRESH:
            return True
        return False

    @property
    def content(self):
        if self.outdated:
            self._log.info('rebuilding content')
            self._content = self.build()
            self._last = datetime.utcnow()
        return self._content

    def update(self):
        self._log.info('updating content')
        self._content = {
            **self.content,
            'state': self.get_state(),
            'events': self.get_events(),
        }
        self._last = datetime.utcnow()

    def reset(self):
        self._log.info('resetting content')
        self._content = None
        self.update()
