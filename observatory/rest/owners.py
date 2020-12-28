from flask import Blueprint

from observatory.models.user import User
from observatory.rest.generic import (
    GenericListing,
    UserSingle,
    user_listing,
    user_single,
)
from observatory.start.extensions import REST

BP_REST_OWNERS = Blueprint('owners', __name__)


@REST.resource('/user', endpoint='api.owners.listing')
class OwnersListing(GenericListing):
    Model = User
    LISTING_GET = user_listing(endpoint='api.owners.single')


@REST.resource('/user/<string:username>', endpoint='api.owners.single')
class OwnersSingle(UserSingle):
    Model = User
    SINGLE_GET = user_single('latest', {})


@REST.resource('/user/<string:username>/points', endpoint='api.owners.points')
class OwnersPoints(UserSingle):
    Model = User
    SINGLE_GET = user_single('points', [])
