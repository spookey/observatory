from flask import Blueprint

from stats.models.prompt import Prompt
from stats.rest.generic import (
    CommonSingle, GenericListing, common_listing, common_single
)
from stats.start.extensions import REST

BP_REST_PROMPT = Blueprint('prompt', __name__)


@REST.resource('/prompt', endpoint='api.prompt.listing')
class PromptListing(GenericListing):
    Model = Prompt
    LISTING_GET = common_listing('api.prompt.single')


@REST.resource('/prompt/<slug>', endpoint='api.prompt.single')
class PromptSingle(CommonSingle):
    Model = Prompt
    SINGLE_GET = common_single()
