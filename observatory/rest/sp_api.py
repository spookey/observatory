from logging import getLogger

from flask import Blueprint, current_app
from flask_restful import Resource, abort, marshal
from flask_restful.fields import Boolean, Float, Integer, List, Nested, String

from observatory.instance import SPACE_API
from observatory.start.extensions import REST

BP_REST_SP_API = Blueprint('space_api', __name__)


@REST.resource('/space.json', endpoint='api.sp_api.json')
class SpaceApi(Resource):
    @staticmethod
    def get():
        if not current_app.config.get('SP_API_ENABLE', False):
            abort(404)

        space = SpaceSchema(SPACE_API.content)
        return (
            marshal(
                space.content,
                space.schema,
            ),
            200 if space.valid else 202,
        )


# pylint: disable=too-many-public-methods


class SpaceSchema:
    def __init__(self, content):
        self._log = getLogger(self.__class__.__name__)

        self.content = content
        self.valid = True

    def invalidate(self, reason):
        self.valid = False
        self._log.warning('invalidating schema: [%s]', reason)

    @property
    def info(self):
        res = {
            'space': String(default=''),
            'logo': String(default=''),
            'url': String(default=''),
        }
        if any(self.content.get(key, None) is None for key in res):
            self.invalidate('missing basic information')
        return res

    @property
    def location(self):
        base = self.content.get('location', {})
        res = {
            'lat': Float(default=0),
            'lon': Float(default=0),
        }
        if any(base.get(key, None) is None for key in res):
            self.invalidate('missing required location data')

        for key in ('address', 'timezone'):
            if base.get(key, None) is not None:
                res.update({key: String(default='')})

        return {'location': Nested(nested=res)}

    @property
    def spacefed(self):
        base = self.content.get('spacefed', {})
        res = {
            'spacenet': Boolean(default=False),
            'spacesaml': Boolean(default=False),
        }
        if not any(base.get(key, None) is not None for key in res):
            return {}

        return {'spacefed': Nested(nested=res, default={})}

    @property
    def cam(self):
        base = self.content.get('cam', [])
        if not base:
            return {}

        return {'cam': List(String(attribute='value', default=''), default=[])}

    @property
    def state_icon(self):
        pre_base = self.content.get('state', {})
        base = pre_base.get('icon', {})
        if not pre_base or not base:
            return {}

        res = {
            'open': String(default=''),
            'closed': String(default=''),
        }
        if any(base.get(key, None) is None for key in res):
            self.invalidate('missing required state icons')
            return {}

        return {'icon': Nested(nested=res)}

    @property
    def state(self):
        base = self.content.get('state', {})
        res = {}
        for key, obj in {
            'open': Boolean(default=False),
            'lastchange': Integer(default=0),
            'trigger_person': String(default=''),
            'message': String(default=''),
        }.items():
            if base.get(key, None) is not None:
                res.update({key: obj})

        res.update({**self.state_icon})
        if not res:
            return {}

        return {'state': Nested(nested=res)}

    @property
    def events(self):
        base = self.content.get('events', [])
        if not base:
            return {}

        res = {
            'name': String(default=''),
            'type': String(default=''),
            'timestamp': Integer(default=0),
        }
        for elem in base:
            if any(elem.get(key, None) is None for key in res):
                self.invalidate('missing required events information')

            if elem.get('extra', None) is not None:
                res.update({'extra': String(default='')})

        return {'events': List(Nested(nested=res), default=[])}

    @property
    def _contact_keymasters(self):
        pre_base = self.content.get('contact', {})
        base = pre_base.get('keymasters', [])
        if not pre_base or not base:
            return {}

        res = {}
        keys = (
            'irc_nick',
            'phone',
            'email',
            'twitter',
        )
        for elem in base:
            if all(elem.get(key, None) is None for key in keys):
                self.invalidate(
                    'missing one of the required keymasters fields'
                )

            for key in (
                *keys,
                'name',
                'xmpp',
                'mastodon',
                'matrix',
            ):
                if elem.get(key, None) is not None:
                    res.update({key: String(default='')})

        if not res:
            return {}

        return {'keymasters': List(Nested(nested=res), default=[])}

    @property
    def contact(self):
        base = self.content.get('contact', {})
        res = {}
        keys = (
            'email',
            'issue_mail',
            'twitter',
            'ml',
        )
        if all(base.get(key, None) is None for key in keys):
            self.invalidate('missing one of the required contact fields')

        for key in (
            *keys,
            'phone',
            'sip',
            'irc',
            'mastodon',
            'facebook',
            'identica',
            'foursquare',
            'xmpp',
            'gopher',
            'matrix',
            'mumble',
        ):
            if base.get(key, None) is not None:
                res.update({key: String(default='')})

        res.update(**self._contact_keymasters)
        return {'contact': Nested(nested=res)}

    def _sensors_generic(self, field, *, req, opt, extra=None):
        pre_base = self.content.get('sensors', {})
        base = pre_base.get(field, [])
        if not base or not pre_base:
            return {}

        res = {**req}
        for elem in base:
            if any(elem.get(key, None) is None for key in res):
                self.invalidate('missing required sensors information')

            if extra is not None:
                res.update(extra(elem))

            for key, obj in opt.items():
                if elem.get(key, None) is not None:
                    res.update({key: obj})

        return {field: List(Nested(nested=res), default=[])}

    def _sensors_radiation_generic(self, field):
        root_base = self.content.get('sensors', {})
        pre_base = root_base.get('radiation', {})
        base = pre_base.get(field, {})
        if not root_base or not pre_base or not base:
            return {}

        res = {
            'value': Float(default=0),
            'unit': String(default=''),
        }
        for elem in base:
            if any(elem.get(key, None) is None for key in res):
                self.invalidate(
                    'missing required radiation sensors information'
                )

            for key, obj in {
                'dead_time': Integer(default=0),
                'conversion_factor': Integer(default=0),
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            }.items():
                if elem.get(key, None) is not None:
                    res.update({key: obj})

        return {field: List(Nested(nested=res), default=[])}

    @property
    def _sensors_temperature(self):
        return self._sensors_generic(
            'temperature',
            req={
                'value': Float(default=0),
                'unit': String(default=''),
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_door_locked(self):
        return self._sensors_generic(
            'door_locked',
            req={
                'value': Boolean(default=True),
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_barometer(self):
        return self._sensors_generic(
            'barometer',
            req={
                'value': Float(default=0),
                'unit': String(default=''),
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_radiation(self):
        pre_base = self.content.get('sensors', {})
        base = pre_base.get('radiation', {})
        if not pre_base or not base:
            return {}

        res = {
            **self._sensors_radiation_generic('alpha'),
            **self._sensors_radiation_generic('beta'),
            **self._sensors_radiation_generic('gamma'),
            **self._sensors_radiation_generic('beta_gamma'),
        }
        if not res:
            return {}

        return {'radiation': Nested(nested=res)}

    @property
    def _sensors_humidity(self):
        return self._sensors_generic(
            'humidity',
            req={
                'value': Float(default=0),
                'unit': String(default=''),
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_beverage_supply(self):
        return self._sensors_generic(
            'beverage_supply',
            req={
                'value': Integer(default=0),
                'unit': String(default=''),
            },
            opt={
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_power_consumption(self):
        return self._sensors_generic(
            'power_consumption',
            req={
                'value': Float(default=0),
                'unit': String(default=''),
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_wind(self):
        def _sub(element, field):
            elem = element.get(field, {})
            res = {
                'value': Float(default=0),
                'unit': String(default=''),
            }
            if any(elem.get(key, None) is None for key in res):
                self.invalidate(
                    'missing required wind sensors properties sub information'
                )

            return {field: Nested(nested=res)}

        def _properties(element):
            elem = element.get('properties', {})
            res = {
                **_sub(elem, 'speed'),
                **_sub(elem, 'gust'),
                **_sub(elem, 'direction'),
                **_sub(elem, 'elevation'),
            }
            return {'properties': Nested(nested=res)}

        return self._sensors_generic(
            'wind',
            req={
                'location': String(default=''),
            },
            opt={
                'name': String(default=''),
                'description': String(default=''),
            },
            extra=_properties,
        )

    @property
    def _sensors_network_connections(self):
        def _machines(element):
            elems = element.get('machines', [])
            if not elems:
                return {}

            res = {'mac': String(default='')}
            for elem in elems:
                if any(elem.get(key, None) is None for key in res):
                    self.invalidate(
                        'missing required network sensors machines information'
                    )

                if elem.get('name', None) is not None:
                    res.update({'name': String(default=0)})

            return {'machines': List(Nested(nested=res), default=[])}

        return self._sensors_generic(
            'network_connections',
            req={
                'value': Integer(default=0),
            },
            opt={
                'type': String(default=''),
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
            extra=_machines,
        )

    @property
    def _sensors_account_balance(self):
        return self._sensors_generic(
            'account_balance',
            req={
                'value': Float(default=0),
                'unit': String(default=''),
            },
            opt={
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_total_member_count(self):
        return self._sensors_generic(
            'total_member_count',
            req={
                'value': Integer(default=0),
            },
            opt={
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
        )

    @property
    def _sensors_people_now_present(self):
        def _names(element):
            elems = element.get('names', [])
            if not elems:
                return {}

            return {'names': List(String(default=''), default=[])}

        return self._sensors_generic(
            'people_now_present',
            req={
                'value': Integer(default=0),
            },
            opt={
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
            extra=_names,
        )

    @property
    def _sensors_network_traffic(self):
        def _bps(element):
            elem = element.get('bits_per_second', {})
            res = {'value': Integer(default=0)}
            if any(elem.get(key, None) is None for key in res):
                self.invalidate(
                    'missing required sensors network traffic '
                    'properties bps value information'
                )

            if elem.get('maximum', None) is not None:
                res.update({'maximum': Integer(default=0)})

            return {'bits_per_second': Nested(nested=res)}

        def _pps(element):
            elem = element.get('packets_per_second', {})
            res = {'value': Integer(default=0)}
            if any(elem.get(key, None) is None for key in res):
                self.invalidate(
                    'missing required sensors network traffic '
                    'properties pps value information'
                )

            return {'packets_per_second': Nested(nested=res)}

        def _properties(element):
            elem = element.get('properties', {})
            if not elem:
                self.invalidate(
                    'missing required sensors network traffic '
                    'properties information'
                )
            res = {
                **_bps(elem),
                **_pps(elem),
            }
            return {'properties': Nested(nested=res)}

        return self._sensors_generic(
            'network_traffic',
            req={},
            opt={
                'location': String(default=''),
                'name': String(default=''),
                'description': String(default=''),
            },
            extra=_properties,
        )

    @property
    def sensors(self):
        base = self.content.get('sensors', {})
        if not base:
            return {}

        res = {
            **self._sensors_temperature,
            **self._sensors_door_locked,
            **self._sensors_barometer,
            **self._sensors_radiation,
            **self._sensors_humidity,
            **self._sensors_beverage_supply,
            **self._sensors_power_consumption,
            **self._sensors_wind,
            **self._sensors_network_connections,
            **self._sensors_account_balance,
            **self._sensors_total_member_count,
            **self._sensors_people_now_present,
            **self._sensors_network_traffic,
        }
        if not res:
            return {}

        return {'sensors': Nested(nested=res)}

    def _feeds(self, field):
        pre_base = self.content.get('feeds', {})
        base = pre_base.get(field, {})
        if not pre_base or not base:
            return {}

        res = {'url': String(default='')}
        if any(base.get(key, None) is None for key in res):
            return {}

        if base.get('type', None) is not None:
            res.update({'type': String(default='')})

        return {field: Nested(nested=res)}

    @property
    def feeds(self):
        base = self.content.get('feeds', {})
        if not base:
            return {}

        res = {
            **self._feeds('blog'),
            **self._feeds('wiki'),
            **self._feeds('calendar'),
            **self._feeds('flickr'),
        }
        if not res:
            return {}

        return {'feeds': Nested(nested=res)}

    @property
    def projects(self):
        base = self.content.get('projects', [])
        if not base:
            return {}

        return {
            'projects': List(String(attribute='value', default=''), default=[])
        }

    @property
    def links(self):
        base = self.content.get('links', [])
        if not base:
            return {}

        res = {
            'name': String(default=''),
            'url': String(default=''),
        }
        for elem in base:
            if any(elem.get(key, None) is None for key in res):
                self.invalidate('missing required links information')

            if elem.get('description', None) is not None:
                res.update({'description': String(default='')})

        return {'links': List(Nested(nested=res), default=[])}

    @property
    def membership_plans(self):
        base = self.content.get('membership_plans', [])
        if not base:
            return {}

        res = {
            'name': String(default=''),
            'value': Float(default=0),
            'currency': String(default=''),
            'billing_interval': String(default=''),
        }
        for elem in base:
            if any(elem.get(key, None) is None for key in res):
                self.invalidate(
                    'missing required membership plans information'
                )

            if elem.get('description', None) is not None:
                res.update({'description': String(default='')})

        return {'membership_plans': List(Nested(nested=res), default=[])}

    @property
    def schema(self):
        self._log.info('building schema')
        return {
            'api_compatibility': List(String(default=''), default=['14']),
            **self.info,
            **self.location,
            **self.spacefed,
            **self.cam,
            **self.state,
            **self.events,
            **self.contact,
            **self.sensors,
            **self.feeds,
            **self.projects,
            **self.links,
            **self.membership_plans,
        }
