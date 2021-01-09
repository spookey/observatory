from flask import url_for
from flask_restful import marshal
from flask_restful.fields import Boolean, String, Url
from pytest import mark

from observatory.rest.owners import OwnersListing

ENDPOINT = 'api.owners.listing'


@mark.usefixtures('session')
class TestOwnersListing:
    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_endpoint():
        assert url_for(ENDPOINT) == '/api/user'

    @staticmethod
    def test_marshal():
        mdef = OwnersListing.LISTING_GET
        assert isinstance(mdef['name'], String)
        assert isinstance(mdef['active'], Boolean)
        url = mdef['url']
        assert isinstance(url, Url)
        assert url.absolute is True
        assert url.endpoint == 'api.owners.single'

    @staticmethod
    def test_get_empty(visitor):
        res = visitor(ENDPOINT)
        assert res.json == []

    @staticmethod
    def test_get_listing(visitor, gen_user):
        one = gen_user(username='one')
        two = gen_user(username='two')
        commons = [two, one]  # newest first, query is sorted
        res = visitor(ENDPOINT)
        assert res.json == marshal(commons, OwnersListing.LISTING_GET)
