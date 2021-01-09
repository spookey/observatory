from datetime import datetime
from logging import getLogger

from observatory.models.mapper import EnumConvert, EnumHorizon
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX, SP_API_REFRESH

# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods


class SpaceApi:
    def __init__(self):
        self._log = getLogger(self.__class__.__name__)

        self._content = None
        self._last = None

    @staticmethod
    def _by_key(key):
        return Value.by_key(key=f'{SP_API_PREFIX}.{key}')

    @staticmethod
    def _get(key, idx=0):
        return Value.get(key=f'{SP_API_PREFIX}.{key}', idx=idx)

    def _get_all(self, key):
        return [
            {
                '_idx': elem.idx,
                'value': elem.elem,
            }
            for elem in self._by_key(key)
            if elem is not None
        ]

    def latest_value(
        self, key, *, idx=0, horizon_key, convert_key, elevate_key
    ):
        sensor = self._get(key, idx=idx)
        if sensor is None or sensor.latest is None:
            return None

        elevate = self._get(elevate_key, idx=idx)
        if elevate is None or not isinstance(elevate, (int, float)):
            elevate = 1.0

        return sensor.latest.translate(
            horizon=EnumHorizon.from_text(self._get(horizon_key, idx=idx)),
            convert=EnumConvert.from_text(self._get(convert_key, idx=idx)),
            elevate=elevate,
            numeric=False,
        )

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
    def contact_keymasters_indices(self):
        return self._indices_any(
            'contact.keymasters.irc_nick',
            'contact.keymasters.phone',
            'contact.keymasters.email',
            'contact.keymasters.twitter',
        )

    @property
    def sensors_temperature_indices(self):
        return self._indices_all(
            'sensors.temperature.value',
            'sensors.temperature.unit',
            'sensors.temperature.location',
        )

    @property
    def sensors_door_locked_indices(self):
        return self._indices_all(
            'sensors.door_locked.value', 'sensors.door_locked.location'
        )

    @property
    def sensors_barometer_indices(self):
        return self._indices_all(
            'sensors.barometer.value',
            'sensors.barometer.unit',
            'sensors.barometer.location',
        )

    @property
    def sensors_humidity_indices(self):
        return self._indices_all(
            'sensors.humidity.value',
            'sensors.humidity.unit',
            'sensors.humidity.location',
        )

    @property
    def sensors_beverage_supply_indices(self):
        return self._indices_all(
            'sensors.beverage_supply.value',
            'sensors.beverage_supply.unit',
        )

    @property
    def sensors_power_consumption_indices(self):
        return self._indices_all(
            'sensors.power_consumption.value',
            'sensors.power_consumption.unit',
            'sensors.power_consumption.location',
        )

    @property
    def sensors_account_balance_indices(self):
        return self._indices_all(
            'sensors.account_balance.value',
            'sensors.account_balance.unit',
        )

    @property
    def sensors_total_member_count_indices(self):
        return self._indices_all('sensors.total_member_count.value')

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

    def get_state(self):
        self._log.info('gathering state')
        return {
            'icon': {
                'open': self._get('state.icon.open'),
                'closed': self._get('state.icon.closed'),
            },
        }

    def get_events(self):
        self._log.info('gathering events')
        return []

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
            'state': self.get_state(),
            'events': self.get_events(),
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
                    for idx in self.contact_keymasters_indices
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
                'temperature': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.temperature.value',
                            idx=idx,
                            horizon_key='sensors.temperature.value.horizon',
                            convert_key='sensors.temperature.value.convert',
                            elevate_key='sensors.temperature.value.elevate',
                        ),
                        'unit': self._get('sensors.temperature.unit', idx=idx),
                        'location': self._get(
                            'sensors.temperature.location', idx=idx
                        ),
                        'name': self._get('sensors.temperature.name', idx=idx),
                        'description': self._get(
                            'sensors.temperature.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_temperature_indices
                ],
                'door_locked': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.door_locked.value',
                            idx=idx,
                            horizon_key='sensors.door_locked.value.horizon',
                            convert_key='sensors.door_locked.value.convert',
                            elevate_key='sensors.door_locked.value.elevate',
                        ),
                        'location': self._get(
                            'sensors.door_locked.location', idx=idx
                        ),
                        'name': self._get('sensors.door_locked.name', idx=idx),
                        'description': self._get(
                            'sensors.door_locked.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_door_locked_indices
                ],
                'barometer': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.barometer.value',
                            idx=idx,
                            horizon_key='sensors.barometer.value.horizon',
                            convert_key='sensors.barometer.value.convert',
                            elevate_key='sensors.barometer.value.elevate',
                        ),
                        'unit': self._get('sensors.barometer.unit', idx=idx),
                        'location': self._get(
                            'sensors.barometer.location', idx=idx
                        ),
                        'name': self._get('sensors.barometer.name', idx=idx),
                        'description': self._get(
                            'sensors.barometer.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_barometer_indices
                ],
                'radiation': {
                    'alpha': [],
                    'beta': [],
                    'gamma': [],
                    'beta_gamma': [],
                },
                'humidity': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.humidity.value',
                            idx=idx,
                            horizon_key='sensors.humidity.value.horizon',
                            convert_key='sensors.humidity.value.convert',
                            elevate_key='sensors.humidity.value.elevate',
                        ),
                        'unit': self._get('sensors.humidity.unit', idx=idx),
                        'location': self._get(
                            'sensors.humidity.location', idx=idx
                        ),
                        'name': self._get('sensors.humidity.name', idx=idx),
                        'description': self._get(
                            'sensors.humidity.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_humidity_indices
                ],
                'beverage_supply': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.beverage_supply.value',
                            idx=idx,
                            horizon_key=(
                                'sensors.beverage_supply.value.horizon'
                            ),
                            convert_key=(
                                'sensors.beverage_supply.value.convert'
                            ),
                            elevate_key=(
                                'sensors.beverage_supply.value.elevate'
                            ),
                        ),
                        'unit': self._get(
                            'sensors.beverage_supply.unit', idx=idx
                        ),
                        'location': self._get(
                            'sensors.beverage_supply.location', idx=idx
                        ),
                        'name': self._get(
                            'sensors.beverage_supply.name', idx=idx
                        ),
                        'description': self._get(
                            'sensors.beverage_supply.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_beverage_supply_indices
                ],
                'power_consumption': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.power_consumption.value',
                            idx=idx,
                            horizon_key=(
                                'sensors.power_consumption.value.horizon'
                            ),
                            convert_key=(
                                'sensors.power_consumption.value.convert'
                            ),
                            elevate_key=(
                                'sensors.power_consumption.value.elevate'
                            ),
                        ),
                        'unit': self._get(
                            'sensors.power_consumption.unit', idx=idx
                        ),
                        'location': self._get(
                            'sensors.power_consumption.location', idx=idx
                        ),
                        'name': self._get(
                            'sensors.power_consumption.name', idx=idx
                        ),
                        'description': self._get(
                            'sensors.power_consumption.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_power_consumption_indices
                ],
                'wind': [],
                'network_connections': [],
                'account_balance': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.account_balance.value',
                            idx=idx,
                            horizon_key=(
                                'sensors.account_balance.value.horizon'
                            ),
                            convert_key=(
                                'sensors.account_balance.value.convert'
                            ),
                            elevate_key=(
                                'sensors.account_balance.value.elevate'
                            ),
                        ),
                        'unit': self._get(
                            'sensors.account_balance.unit', idx=idx
                        ),
                        'location': self._get(
                            'sensors.account_balance.location', idx=idx
                        ),
                        'name': self._get(
                            'sensors.account_balance.name', idx=idx
                        ),
                        'description': self._get(
                            'sensors.account_balance.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_account_balance_indices
                ],
                'total_member_count': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            'sensors.total_member_count.value',
                            idx=idx,
                            horizon_key='sensors.total_member_count.horizon',
                            convert_key='sensors.total_member_count.convert',
                            elevate_key='sensors.total_member_count.elevate',
                        ),
                        'location': self._get(
                            'sensors.total_member_count.location', idx=idx
                        ),
                        'name': self._get(
                            'sensors.total_member_count.name', idx=idx
                        ),
                        'description': self._get(
                            'sensors.total_member_count.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_total_member_count_indices
                ],
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

    def clear(self):
        self._content = None
        self._last = None
        return all((self._content is None, self._last is None))

    def reset(self):
        self._log.info('resetting content')
        self.clear()
        return self.content
