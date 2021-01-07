from collections.abc import Mapping
from copy import deepcopy
from json import dumps, loads

from flask_restful import marshal
from pytest import fixture, mark, raises

from observatory.rest.sp_api import SpaceSchema

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-public-methods


@fixture(scope='function')
def merge():
    def func(original, update):
        assert isinstance(original, Mapping)
        assert isinstance(update, Mapping)

        res = dict(deepcopy(original))
        for key, val in update.items():
            if isinstance(val, Mapping):
                res[key] = func(res.get(key, {}), val)
            else:
                res[key] = val
        return res

    yield func


class TestTestMerge:
    @staticmethod
    def test_empty(merge):
        assert merge({}, {}) == {}

    @staticmethod
    @mark.parametrize('val', [1337, None, True, 'text', open])
    def test_fails_on_non_dicts(merge, val):
        with raises(AssertionError):
            merge(val, {})

        with raises(AssertionError):
            merge({}, val)

    @staticmethod
    def test_merge_distinct(merge):
        assert merge({1: 2}, {3: 4}) == {1: 2, 3: 4}

    @staticmethod
    def test_merge_overwrites(merge):
        assert merge({1: 2}, {1: 3}) == {1: 3}
        assert merge({1: 3}, {1: 2}) == {1: 2}

    @staticmethod
    def test_nested(merge):
        assert merge({1: 2, 3: {4: 5}}, {1: 7, 3: {9: 0, 4: 8}}) == {
            1: 7,
            3: {4: 8, 9: 0},
        }
        assert (
            merge(
                {1: {2: {3: {4: {5: {6: {7: 8}}}}}}},
                {1: {2: {3: {4: {5: {6: {9: 0}}}}}}},
            )
            == {1: {2: {3: {4: {5: {6: {7: 8, 9: 0}}}}}}}
        )

    @staticmethod
    def test_original_stays(merge):
        org = {1: 2}
        nxt = {1: 0}
        assert merge(org, nxt) == {1: 0}
        assert org == {1: 2}
        assert nxt == {1: 0}


class SpaceObj:
    def __init__(self, content=None):
        self._cnt = content if content is not None else {}
        self._obj = None

    @property
    def content(self):
        return self._cnt

    @content.setter
    def content(self, new_content):
        self._cnt = new_content
        self._obj = None

    @property
    def obj(self):
        if self._obj is None:
            self._obj = SpaceSchema(self.content)
        return self._obj

    @property
    def is_valid(self):
        assert self.obj.valid is True
        return True

    @property
    def is_invalid(self):
        assert self.obj.valid is False
        return True

    def make(self, schema, readable=True):
        res = marshal(self.content, schema)
        return res if not readable else loads(dumps(res))


@fixture(scope='function')
def space():
    yield SpaceObj


class TestSpaceApiSchema:
    @staticmethod
    def test_initial(space):
        spc = space({'not': 'empty'})

        assert spc.obj.content == spc.content
        assert spc.is_valid

    @staticmethod
    def test_invalidate(space):
        spc = space()
        assert spc.is_valid

        spc.obj.invalidate('testing')
        assert spc.is_invalid

    @staticmethod
    def test_info(space):
        spc = space()
        empty = {'space': '', 'logo': '', 'url': ''}

        assert spc.make(spc.obj.info) == empty
        assert spc.is_invalid

        spc.content = empty
        assert spc.make(spc.obj.info) == empty
        assert spc.is_valid

    @staticmethod
    def test_location(space, merge):
        spc = space()
        empty = {'location': {'lat': 0, 'lon': 0}}

        assert spc.make(spc.obj.location) == empty
        assert spc.is_invalid

        spc.content = empty
        assert spc.make(spc.obj.location) == empty
        assert spc.is_valid

        filled = merge(empty, {'location': {'address': '', 'timezone': ''}})
        spc.content = filled
        assert spc.make(spc.obj.location) == filled
        assert spc.is_valid

    @staticmethod
    def test_spacefed(space):
        spc = space()
        empty = {'spacefed': {'spacenet': False, 'spacesaml': False}}

        assert spc.make(spc.obj.spacefed) == {}
        assert spc.is_valid

        spc.content = empty
        assert spc.make(spc.obj.spacefed) == empty
        assert spc.is_valid

    @staticmethod
    def test_cam(space):
        def _wrap(*elems):
            return {'cam': list(elems)}

        spc = space()

        assert spc.make(spc.obj.cam) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.cam) == {}
        assert spc.is_valid

        spc.content = _wrap({'wrong': 'data'}, {'also': 'wrong'})
        assert spc.make(spc.obj.cam) == _wrap('', '')
        assert spc.is_valid

        spc.content = _wrap(
            {'ignored': 'data', 'elem': 'cam1'}, {'elem': 'cam2'}
        )
        assert spc.make(spc.obj.cam) == _wrap('cam1', 'cam2')
        assert spc.is_valid

    @staticmethod
    def test_state_icon(space):
        spc = space()
        empty = {'icon': {'open': '', 'closed': ''}}

        assert spc.make(spc.obj.state_icon) == {}
        assert spc.is_valid

        spc.content = {'state': {}}
        assert spc.make(spc.obj.state_icon) == {}
        assert spc.is_valid

        spc.content = {'state': {'icon': {}}}
        assert spc.make(spc.obj.state_icon) == {}
        assert spc.is_valid

        spc.content = {'state': {'icon': {'wrong': 'value'}}}
        assert spc.make(spc.obj.state_icon) == {}
        assert spc.is_invalid

        spc.content = {'state': empty}
        assert spc.make(spc.obj.state_icon) == empty
        assert spc.is_valid

    @staticmethod
    def test_state(space, merge):
        spc = space()

        assert spc.make(spc.obj.state) == {}
        assert spc.is_valid

        spc.content = {'state': {}}
        assert spc.make(spc.obj.state) == {}
        assert spc.is_valid

        partial = {'state': {'open': False}}
        spc.content = partial
        assert spc.make(spc.obj.state) == partial
        assert spc.is_valid

        filled = merge(
            partial,
            {
                'state': {
                    'lastchange': 0,
                    'trigger_person': '',
                    'message': '',
                }
            },
        )

        spc.content = filled
        assert spc.make(spc.obj.state) == filled
        assert spc.is_valid

        spc.content = merge(filled, {'state': {'icon': {'wrong': 'content'}}})
        assert spc.make(spc.obj.state) == filled
        assert spc.is_invalid

        with_icon = merge(
            filled, {'state': {'icon': {'open': '', 'closed': ''}}}
        )
        spc.content = with_icon
        assert spc.make(spc.obj.state) == with_icon
        assert spc.is_valid

    @staticmethod
    def test_events(space, merge):
        def _wrap(*elems):
            return {'events': list(elems)}

        spc = space()

        assert spc.make(spc.obj.events) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.events) == {}
        assert spc.is_valid

        partial = {'name': '', 'timestamp': 0}
        correct = merge(partial, {'type': ''})

        spc.content = _wrap(partial)
        assert spc.make(spc.obj.events) == _wrap(correct)
        assert spc.is_invalid

        spc.content = _wrap(correct)
        assert spc.make(spc.obj.events) == _wrap(correct)
        assert spc.is_valid

        extra = merge(correct, {'extra': ''})
        spc.content = _wrap(correct, extra)
        assert spc.make(spc.obj.events) == _wrap(extra, extra)
        assert spc.is_valid

    @staticmethod
    def test_contact(space, merge):
        spc = space()

        assert spc.make(spc.obj.contact) == {'contact': {}}
        assert spc.is_invalid

        partial = {'contact': {'irc': ''}}
        spc.content = partial
        assert spc.make(spc.obj.contact) == partial
        assert spc.is_invalid

        correct = {'contact': {'email': ''}}
        spc.content = correct
        assert spc.make(spc.obj.contact) == correct
        assert spc.is_valid

        irrelevant = merge(correct, {'contact': {'wrong': 'value'}})
        spc.content = irrelevant
        assert spc.make(spc.obj.contact) == correct
        assert spc.is_valid

    @staticmethod
    def test_contact_keymasters(space, merge):
        no_keymasters = {'contact': {'ml': ''}}

        def _wrap(*elems):
            return merge(
                no_keymasters, {'contact': {'keymasters': list(elems)}}
            )

        spc = space()

        assert spc.make(spc.obj.contact) == {'contact': {}}
        assert spc.is_invalid

        spc.content = _wrap()
        assert spc.make(spc.obj.contact) == no_keymasters
        assert spc.is_valid

        spc.content = _wrap({'unrelated': 'data'})
        assert spc.make(spc.obj.contact) == no_keymasters
        assert spc.is_invalid

        inner_missing = {'xmpp': ''}
        missing = _wrap(inner_missing)
        spc.content = missing
        assert spc.make(spc.obj.contact) == missing
        assert spc.is_invalid

        inner_correct = {'email': ''}
        correct = _wrap(inner_correct)
        spc.content = correct
        assert spc.make(spc.obj.contact) == correct
        assert spc.is_valid

        merged = merge(inner_missing, inner_correct)
        spc.content = _wrap(inner_missing, inner_correct)
        assert spc.make(spc.obj.contact) == _wrap(merged, merged)
        assert spc.is_invalid

    @staticmethod
    @mark.parametrize(
        ('field', 'required', 'optional', 'special'),
        [
            (
                'temperature',
                {'value': 0, 'unit': '', 'location': ''},
                {'name': '', 'description': ''},
                None,
            ),
            (
                'door_locked',
                {'value': True, 'location': ''},
                {'name': '', 'description': ''},
                None,
            ),
            (
                'barometer',
                {'value': 0, 'unit': '', 'location': ''},
                {'name': '', 'description': ''},
                None,
            ),
            (
                'humidity',
                {'value': 0, 'unit': '', 'location': ''},
                {'name': '', 'description': ''},
                None,
            ),
            (
                'beverage_supply',
                {'value': 0, 'unit': ''},
                {'location': '', 'name': '', 'description': ''},
                None,
            ),
            (
                'power_consumption',
                {'value': 0, 'unit': '', 'location': ''},
                {'name': '', 'description': ''},
                None,
            ),
            (
                'wind',
                {
                    'location': '',
                    'properties': {
                        'speed': {'value': 0, 'unit': ''},
                        'gust': {'value': 0, 'unit': ''},
                        'direction': {'value': 0, 'unit': ''},
                        'elevation': {'value': 0, 'unit': ''},
                    },
                },
                {'name': '', 'description': ''},
                None,
            ),
            (
                'network_connections',
                {
                    'value': 0,
                },
                {
                    'type': '',
                    'location': '',
                    'name': '',
                    'description': '',
                    'machines': [{'mac': '', 'name': ''}],
                },
                (
                    {'value': 0, 'machines': [{'name': ''}]},
                    {'value': 0, 'machines': [{'mac': '', 'name': ''}]},
                ),
            ),
            (
                'account_balance',
                {'value': 0, 'unit': ''},
                {'location': '', 'name': '', 'description': ''},
                None,
            ),
            (
                'total_member_count',
                {'value': 0},
                {'location': '', 'name': '', 'description': ''},
                None,
            ),
            (
                'people_now_present',
                {'value': 0},
                {
                    'location': '',
                    'name': '',
                    'description': '',
                    'names': [''],
                },
                None,
            ),
            (
                'network_traffic',
                {
                    'properties': {
                        'bits_per_second': {'value': 0},
                        'packets_per_second': {'value': 0},
                    }
                },
                {'location': '', 'name': '', 'description': ''},
                (
                    {
                        'properties': {
                            'bits_per_second': {'value': 0, 'maximum': 0},
                        }
                    },
                    {
                        'properties': {
                            'bits_per_second': {'value': 0, 'maximum': 0},
                            'packets_per_second': {'value': 0},
                        }
                    },
                ),
            ),
        ],
    )
    def test_sensors(space, merge, field, required, optional, special):
        def _wrap(*elems):
            return {'sensors': {field: list(elems)}}

        spc = space()
        assert spc.make(spc.obj.sensors) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.sensors) == {}
        assert spc.is_valid

        spc.content = _wrap(required)
        assert spc.make(spc.obj.sensors) == _wrap(required)
        assert spc.is_valid

        spc.content = _wrap({'irrelevant': 'content'})
        assert spc.make(spc.obj.sensors) == _wrap(required)
        assert spc.is_invalid

        spc.content = _wrap(optional)
        assert spc.make(spc.obj.sensors) == _wrap(merge(optional, required))
        assert spc.is_invalid

        if special:
            req, res = special
            spc.content = _wrap(req)
            assert spc.make(spc.obj.sensors) == _wrap(res)
            assert spc.is_invalid

    @staticmethod
    @mark.parametrize('field', ('alpha', 'beta', 'gamma', 'beta_gamma'))
    def test_sensors_radiation(space, field, merge):
        def _wrap(*elems):
            return {'sensors': {'radiation': {field: list(elems)}}}

        spc = space()

        assert spc.make(spc.obj.sensors) == {}
        assert spc.is_valid

        spc.content = {'sensors': {'radiation': {}}}
        assert spc.make(spc.obj.sensors) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.sensors) == {}
        assert spc.is_valid

        required = {'value': 0, 'unit': ''}
        spc.content = _wrap(required)
        assert spc.make(spc.obj.sensors) == _wrap(required)
        assert spc.is_valid

        spc.content = _wrap({'irrelevant': 'content'})
        assert spc.make(spc.obj.sensors) == _wrap(required)
        assert spc.is_invalid

        optional = {
            'dead_time': 0,
            'conversion_factor': 0,
            'location': '',
            'name': '',
            'description': '',
        }
        spc.content = _wrap(optional)
        assert spc.make(spc.obj.sensors) == _wrap(merge(optional, required))
        assert spc.is_invalid

    @staticmethod
    @mark.parametrize('field', ('blog', 'wiki', 'calendar', 'flickr'))
    def test_feeds(space, field):

        spc = space()

        assert spc.make(spc.obj.feeds) == {}
        assert spc.is_valid

        spc.content = {'feeds': {}}
        assert spc.make(spc.obj.feeds) == {}
        assert spc.is_valid

        spc.content = {'feeds': {field: {}}}
        assert spc.make(spc.obj.feeds) == {}
        assert spc.is_valid

        spc.content = {'feeds': {field: {'wrong': 'value'}}}
        assert spc.make(spc.obj.feeds) == {}
        assert spc.is_valid

        spc.content = {'feeds': {field: {'type': ''}}}
        assert spc.make(spc.obj.feeds) == {}
        assert spc.is_valid

        spc.content = {'feeds': {field: {'url': ''}}}
        assert spc.make(spc.obj.feeds) == {'feeds': {field: {'url': ''}}}
        assert spc.is_valid

        spc.content = {'feeds': {field: {'url': '', 'type': ''}}}
        assert spc.make(spc.obj.feeds) == {
            'feeds': {field: {'url': '', 'type': ''}}
        }
        assert spc.is_valid

        spc.content = {'feeds': {field: {'url': ''}, 'wrong': {'url': ''}}}
        assert spc.make(spc.obj.feeds) == {'feeds': {field: {'url': ''}}}
        assert spc.is_valid

        inner = {
            feed: {'url': '', 'type': ''}
            for feed in ('blog', 'wiki', 'calendar', 'flickr')
        }
        spc.content = {'feeds': inner}
        assert spc.make(spc.obj.feeds) == {'feeds': inner}
        assert spc.is_valid

    @staticmethod
    def test_projects(space):
        def _wrap(*elems):
            return {'projects': list(elems)}

        spc = space()

        assert spc.make(spc.obj.projects) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.projects) == {}
        assert spc.is_valid

        spc.content = _wrap({'wrong': 'data'}, {'also': 'wrong'})
        assert spc.make(spc.obj.projects) == _wrap('', '')
        assert spc.is_valid

        spc.content = _wrap(
            {'ignored': 'data', 'elem': 'project1'}, {'elem': 'project2'}
        )
        assert spc.make(spc.obj.projects) == _wrap('project1', 'project2')
        assert spc.is_valid

    @staticmethod
    def test_links(space, merge):
        def _wrap(*elems):
            return {'links': list(elems)}

        spc = space()

        assert spc.make(spc.obj.links) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.links) == {}
        assert spc.is_valid

        correct = {'name': '', 'url': ''}
        spc.content = _wrap(correct)
        assert spc.make(spc.obj.links) == _wrap(correct)
        assert spc.is_valid

        spc.content = _wrap({'wrong': 'values'})
        assert spc.make(spc.obj.links) == _wrap(correct)
        assert spc.is_invalid

        extra = {'description': ''}
        spc.content = _wrap(extra)
        assert spc.make(spc.obj.links) == _wrap(merge(correct, extra))
        assert spc.is_invalid

    @staticmethod
    def test_membership_plans(space, merge):
        def _wrap(*elems):
            return {'membership_plans': list(elems)}

        spc = space()

        assert spc.make(spc.obj.membership_plans) == {}
        assert spc.is_valid

        spc.content = _wrap()
        assert spc.make(spc.obj.membership_plans) == {}
        assert spc.is_valid

        correct = {
            'name': '',
            'value': 0,
            'currency': '',
            'billing_interval': '',
        }
        spc.content = _wrap(correct)
        assert spc.make(spc.obj.membership_plans) == _wrap(correct)
        assert spc.is_valid

        extra = {'description': ''}
        spc.content = _wrap(extra)
        assert spc.make(spc.obj.membership_plans) == _wrap(
            merge(correct, extra)
        )
        assert spc.is_invalid

        partial = {
            'value': 0,
            'currency': '',
        }
        spc.content = _wrap(partial)
        assert spc.make(spc.obj.membership_plans) == _wrap(correct)
        assert spc.is_invalid

    @staticmethod
    def test_schema(space, merge):
        spc = space()
        empty = {
            'api_compatibility': ['14'],
            'space': '',
            'logo': '',
            'url': '',
            'location': {'lat': 0, 'lon': 0},
            'contact': {},
        }

        assert spc.make(spc.obj.schema) == empty
        assert spc.is_invalid

        contact = merge(empty, {'contact': {'issue_mail': ''}})
        spc.content = contact
        assert spc.make(spc.obj.schema) == contact
        assert spc.is_valid

        keymasters = merge(
            contact, {'contact': {'keymasters': [{'email': ''}]}}
        )
        spc.content = keymasters
        assert spc.make(spc.obj.schema) == keymasters
        assert spc.is_valid

        projects = merge(keymasters, {'projects': ['', '']})
        spc.content = projects
        assert spc.make(spc.obj.schema) == projects
        assert spc.is_valid

        links = merge(
            projects, {'links': [{'name': '', 'description': '', 'url': ''}]}
        )
        spc.content = links
        assert spc.make(spc.obj.schema) == links
        assert spc.is_valid
