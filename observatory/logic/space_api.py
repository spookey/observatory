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
    def _by_key(*, key):
        return Value.by_key(key=f'{SP_API_PREFIX}.{key}')

    @staticmethod
    def _get(*, key, idx=0):
        return Value.get(key=f'{SP_API_PREFIX}.{key}', idx=idx)

    def _get_all(self, *, key):
        return [
            {
                '_idx': elem.idx,
                'value': elem.elem,
            }
            for elem in self._by_key(key=key)
            if elem is not None
        ]

    def latest_value(self, *, key, idx=0, convert):
        sensor = self._get(key=key, idx=idx)
        if sensor is None or sensor.latest is None:
            return None

        return sensor.latest.translate(
            horizon=EnumHorizon.NORMAL, convert=convert, numeric=False
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

    def sensors_radiation_indices(self, sub):
        return self._indices_all(
            f'sensors.radiation.{sub}.value',
            f'sensors.radiation.{sub}.unit',
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
    def sensors_wind_indices(self):
        return self._indices_all(
            'sensors.wind.properties.speed.value',
            'sensors.wind.properties.speed.unit',
            'sensors.wind.properties.gust.value',
            'sensors.wind.properties.gust.unit',
            'sensors.wind.properties.direction.value',
            'sensors.wind.properties.direction.unit',
            'sensors.wind.properties.elevation.value',
            'sensors.wind.properties.elevation.unit',
            'sensors.wind.location',
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
    def sensors_network_traffic_indices(self):
        return self._indices_any(
            'sensors.network_traffic.properties.bits_per_second.value',
            'sensors.network_traffic.properties.packets_per_second.value',
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

    def get_state(self):
        self._log.info('gathering state')
        return {
            'icon': {
                'open': self._get(key='state.icon.open'),
                'closed': self._get(key='state.icon.closed'),
            },
        }

    def get_events(self):
        self._log.info('gathering events')
        return []

    def build(self):
        return {
            'api_compatibility': ['14'],
            'space': self._get(key='space'),
            'logo': self._get(key='logo'),
            'url': self._get(key='url'),
            'location': {
                'address': self._get(key='location.address'),
                'lat': self._get(key='location.lat'),
                'lon': self._get(key='location.lon'),
                'timezone': self._get(key='location.timezone'),
            },
            'spacefed': {
                'spacenet': self._get(key='spacefed.spacenet'),
                'spacesaml': self._get(key='spacefed.spacesaml'),
            },
            'cam': self._get_all(key='cam'),
            'state': self.get_state(),
            'events': self.get_events(),
            'contact': {
                'phone': self._get(key='contact.phone'),
                'sip': self._get(key='contact.sip'),
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
                'irc': self._get(key='contact.irc'),
                'twitter': self._get(key='contact.twitter'),
                'mastodon': self._get(key='contact.mastodon'),
                'facebook': self._get(key='contact.facebook'),
                'identica': self._get(key='contact.identica'),
                'foursquare': self._get(key='contact.foursquare'),
                'email': self._get(key='contact.email'),
                'ml': self._get(key='contact.ml'),
                'xmpp': self._get(key='contact.xmpp'),
                'issue_mail': self._get(key='contact.issue_mail'),
                'gopher': self._get(key='contact.gopher'),
                'matrix': self._get(key='contact.matrix'),
                'mumble': self._get(key='contact.mumble'),
            },
            'sensors': {
                'temperature': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.temperature.value',
                            idx=idx,
                            convert=EnumConvert.NATURAL,
                        ),
                        'unit': self._get(
                            key='sensors.temperature.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.temperature.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.temperature.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.temperature.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_temperature_indices
                ],
                'door_locked': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.door_locked.value',
                            idx=idx,
                            convert=EnumConvert.BOOLEAN,
                        ),
                        'location': self._get(
                            key='sensors.door_locked.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.door_locked.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.door_locked.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_door_locked_indices
                ],
                'barometer': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.barometer.value',
                            idx=idx,
                            convert=EnumConvert.NATURAL,
                        ),
                        'unit': self._get(
                            key='sensors.barometer.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.barometer.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.barometer.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.barometer.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_barometer_indices
                ],
                'radiation': {
                    sub: [
                        {
                            '_idx': idx,
                            'value': self.latest_value(
                                key=f'sensors.radiation.{sub}.value',
                                idx=idx,
                                convert=EnumConvert.NATURAL,
                            ),
                            'unit': self._get(
                                key=f'sensors.radiation.{sub}.unit', idx=idx
                            ),
                            'dead_time': self._get(
                                key=f'sensors.radiation.{sub}.dead_time',
                                idx=idx,
                            ),
                            'conversion_factor': self._get(
                                key=(
                                    f'sensors.radiation.{sub}.'
                                    'conversion_factor'
                                ),
                                idx=idx,
                            ),
                            'location': self._get(
                                key=f'sensors.radiation.{sub}.location',
                                idx=idx,
                            ),
                            'name': self._get(
                                key=f'sensors.radiation.{sub}.name', idx=idx
                            ),
                            'description': self._get(
                                key=f'sensors.radiation.{sub}.description',
                                idx=idx,
                            ),
                        }
                        for idx in self.sensors_radiation_indices(sub)
                    ]
                    for sub in ['alpha', 'beta', 'gamma', 'beta_gamma']
                },
                'humidity': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.humidity.value',
                            idx=idx,
                            convert=EnumConvert.INTEGER,
                        ),
                        'unit': self._get(
                            key='sensors.humidity.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.humidity.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.humidity.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.humidity.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_humidity_indices
                ],
                'beverage_supply': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.beverage_supply.value',
                            idx=idx,
                            convert=EnumConvert.INTEGER,
                        ),
                        'unit': self._get(
                            key='sensors.beverage_supply.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.beverage_supply.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.beverage_supply.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.beverage_supply.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_beverage_supply_indices
                ],
                'power_consumption': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.power_consumption.value',
                            idx=idx,
                            convert=EnumConvert.INTEGER,
                        ),
                        'unit': self._get(
                            key='sensors.power_consumption.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.power_consumption.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.power_consumption.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.power_consumption.description',
                            idx=idx,
                        ),
                    }
                    for idx in self.sensors_power_consumption_indices
                ],
                'wind': [
                    {
                        '_idx': idx,
                        'properties': {
                            'speed': {
                                'value': self.latest_value(
                                    key='sensors.wind.properties.speed.value',
                                    idx=idx,
                                    convert=EnumConvert.NATURAL,
                                ),
                                'unit': self._get(
                                    key='sensors.wind.properties.speed.unit',
                                    idx=idx,
                                ),
                            },
                            'gust': {
                                'value': self.latest_value(
                                    key='sensors.wind.properties.gust.value',
                                    idx=idx,
                                    convert=EnumConvert.NATURAL,
                                ),
                                'unit': self._get(
                                    key='sensors.wind.properties.gust.unit',
                                    idx=idx,
                                ),
                            },
                            'direction': {
                                'value': self.latest_value(
                                    key=(
                                        'sensors.wind.properties.'
                                        'direction.value'
                                    ),
                                    idx=idx,
                                    convert=EnumConvert.INTEGER,
                                ),
                                'unit': self._get(
                                    key=(
                                        'sensors.wind.properties.'
                                        'direction.unit'
                                    ),
                                    idx=idx,
                                ),
                            },
                            'elevation': {
                                'value': self.latest_value(
                                    key=(
                                        'sensors.wind.properties.'
                                        'elevation.value'
                                    ),
                                    idx=idx,
                                    convert=EnumConvert.INTEGER,
                                ),
                                'unit': self._get(
                                    key=(
                                        'sensors.wind.properties.'
                                        'elevation.unit'
                                    ),
                                    idx=idx,
                                ),
                            },
                        },
                        'location': self._get(
                            key='sensors.wind.location', idx=idx
                        ),
                        'name': self._get(key='sensors.wind.name', idx=idx),
                        'description': self._get(
                            key='sensors.wind.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_wind_indices
                ],
                'network_connections': [],
                'account_balance': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.account_balance.value',
                            idx=idx,
                            convert=EnumConvert.NATURAL,
                        ),
                        'unit': self._get(
                            key='sensors.account_balance.unit', idx=idx
                        ),
                        'location': self._get(
                            key='sensors.account_balance.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.account_balance.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.account_balance.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_account_balance_indices
                ],
                'total_member_count': [
                    {
                        '_idx': idx,
                        'value': self.latest_value(
                            key='sensors.total_member_count.value',
                            idx=idx,
                            convert=EnumConvert.INTEGER,
                        ),
                        'location': self._get(
                            key='sensors.total_member_count.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.total_member_count.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.total_member_count.description',
                            idx=idx,
                        ),
                    }
                    for idx in self.sensors_total_member_count_indices
                ],
                'people_now_present': [],
                'network_traffic': [
                    {
                        '_idx': idx,
                        'properties': {
                            'bits_per_second': {
                                'value': self.latest_value(
                                    key=(
                                        'sensors.network_traffic.properties.'
                                        'bits_per_second.value'
                                    ),
                                    idx=idx,
                                    convert=EnumConvert.NATURAL,
                                ),
                                'maximum': self._get(
                                    key=(
                                        'sensors.network_traffic.properties.'
                                        'bits_per_second.maximum'
                                    ),
                                    idx=idx,
                                ),
                            },
                            'packets_per_second': {
                                'value': self.latest_value(
                                    key=(
                                        'sensors.network_traffic.properties.'
                                        'packets_per_second.value'
                                    ),
                                    idx=idx,
                                    convert=EnumConvert.NATURAL,
                                ),
                            },
                        },
                        'location': self._get(
                            key='sensors.network_traffic.location', idx=idx
                        ),
                        'name': self._get(
                            key='sensors.network_traffic.name', idx=idx
                        ),
                        'description': self._get(
                            key='sensors.network_traffic.description', idx=idx
                        ),
                    }
                    for idx in self.sensors_network_traffic_indices
                ],
            },
            'feeds': {
                'blog': {
                    'type': self._get(key='feeds.blog.type'),
                    'url': self._get(key='feeds.blog.url'),
                },
                'wiki': {
                    'type': self._get(key='feeds.wiki.type'),
                    'url': self._get(key='feeds.wiki.url'),
                },
                'calendar': {
                    'type': self._get(key='feeds.calendar.type'),
                    'url': self._get(key='feeds.calendar.url'),
                },
                'flickr': {
                    'type': self._get(key='feeds.calendar.type'),
                    'url': self._get(key='feeds.calendar.url'),
                },
            },
            'projects': self._get_all(key='projects'),
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
