from datetime import datetime
from logging import getLogger

from observatory.models.values import Values
from observatory.start.environment import SP_API_PREFIX, SP_API_REFRESH


class SpaceApi:
    def __init__(self):
        self._log = getLogger(self.__class__.__name__)
        self._content = None
        self._last = None

    @staticmethod
    def _by_key(key):
        return Values.by_key(key=f'{SP_API_PREFIX}.{key}')

    @staticmethod
    def _get(key, idx=0):
        return Values.get(key=f'{SP_API_PREFIX}.{key}', idx=idx)

    def _get_all(self, key):
        return [{
            '_idx': elem.idx,
            'value': elem.value,
        } for elem in self._by_key(key) if elem is not None]

    def _indices_any(self, *keys):
        result = set()
        for key in keys:
            result = result.union(
                elem.idx for elem in self._by_key(key=key) if elem is not None
            )
        return sorted(result)

    def _indices_all(self, first, *keys):
        result = set(
            elem.idx for elem in self._by_key(key=first) if elem is not None
        )
        for key in keys:
            result = result.intersection(
                elem.idx for elem in self._by_key(key=key) if elem is not None
            )
        return sorted(result)

    @staticmethod
    def next_index(indices):
        if not indices:
            return 0

        top = max(indices)
        diff = set(range(top)).difference(indices)
        if diff:
            return min(diff)

        return 1 + top

    @property
    def cam_indices(self):
        return self._indices_all('cam')

    @property
    def concact_keymasters_indices(self):
        return self._indices_any(
            'contact.keymasters.irc_nick',
            'contact.keymasters.phone',
            'contact.keymasters.email',
            'contact.keymasters.twitter',
        )

    @property
    def projects_indices(self):
        return self._indices_all('projects')

    @property
    def links_indices(self):
        return self._indices_all(
            'links.name',
            'links.url',
        )

    @property
    def membership_plans_indices(self):
        return self._indices_all(
            'membership_plans.name',
            'membership_plans.value',
            'membership_plans.currency',
            'membership_plans.billing_interval',
        )

    def build(self):
        return {
            'api_compatibility': ['14'],
            'space': self._get('space'),
            'logo': self._get('logo'),
            'url': self._get('url'),
            'location': {
                'address': self._get('location.address'),
                'lat': self._get('location.lat'),
                'lon': self._get('location.lon'),
                'timezone': self._get('location.timezone'),
            },
            'spacefed': {
                'spacenet': self._get('spacefed.spacenet'),
                'spacesaml': self._get('spacefed.spacesaml'),
            },
            'cam': self._get_all('cam'),
            'state': {},
            'events': [],
            'contact': {
                'phone': self._get('contact.phone'),
                'sip': self._get('contact.sip'),
                'keymasters': [
                    {
                        '_idx': idx,
                        'name': self._get(
                            key='contact.keymasters.name', idx=idx
                        ),
                        'irc_nick': self._get(
                            key='contact.keymasters.irc_nick', idx=idx
                        ),
                        'phone': self._get(
                            key='contact.keymasters.phone', idx=idx
                        ),
                        'email': self._get(
                            key='contact.keymasters.email', idx=idx
                        ),
                        'twitter': self._get(
                            key='contact.keymasters.twitter', idx=idx
                        ),
                        'xmpp': self._get(
                            key='contact.keymasters.xmpp', idx=idx
                        ),
                        'mastodon': self._get(
                            key='contact.keymasters.mastodon', idx=idx
                        ),
                        'matrix': self._get(
                            key='contact.keymasters.matrix', idx=idx
                        ),
                    }
                    for idx in self.concact_keymasters_indices
                ],
                'irc': self._get('contact.irc'),
                'twitter': self._get('contact.twitter'),
                'mastodon': self._get('contact.mastodon'),
                'facebook': self._get('contact.facebook'),
                'identica': self._get('contact.identica'),
                'foursquare': self._get('contact.foursquare'),
                'email': self._get('contact.email'),
                'ml': self._get('contact.ml'),
                'xmpp': self._get('contact.xmpp'),
                'issue_mail': self._get('contact.issue_mail'),
                'gopher': self._get('contact.gopher'),
                'matrix': self._get('contact.matrix'),
                'mumble': self._get('contact.mumble'),
            },
            'sensors': {
                'temperature': [],
                'door_locked': [],
                'barometer': [],
                'radiation': {},
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
                    'type': self._get('feeds.blog.type'),
                    'url': self._get('feeds.blog.url'),
                },
                'wiki': {
                    'type': self._get('feeds.wiki.type'),
                    'url': self._get('feeds.wiki.url'),
                },
                'calendar': {
                    'type': self._get('feeds.calendar.type'),
                    'url': self._get('feeds.calendar.url'),
                },
                'flickr': {
                    'type': self._get('feeds.calendar.type'),
                    'url': self._get('feeds.calendar.url'),
                },
            },
            'projects': self._get_all('projects'),
            'links': [
                {
                    '_idx': idx,
                    'name': self._get(key='links.name', idx=idx),
                    'description': self._get(key='links.description', idx=idx),
                    'url': self._get(key='links.url', idx=idx),
                }
                for idx in self.links_indices
            ],
            'membership_plans': [
                {
                    '_idx': idx,
                    'name': self._get(key='membership_plans.name', idx=idx),
                    'value': self._get(key='membership_plans.value', idx=idx),
                    'currency': self._get(
                        key='membership_plans.currency', idx=idx
                    ),
                    'billing_interval': self._get(
                        key='membership_plans.billing_interval', idx=idx
                    ),
                    'description': self._get(
                        key='membership_plans.description', idx=idx
                    ),
                }
                for idx in self.membership_plans_indices
            ],
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
        return self.content

    def reset(self):
        self._log.info('resetting content')
        self._content = None
        self._last = None
        return self.update()
