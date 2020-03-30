from flask import Blueprint

from stats.models.prompt import Prompt
from stats.rest.common import (
    CommonListing, CommonSingle, listing_envelope, single_envelope
)
from stats.start.extensions import REST

BP_REST_PROMPT = Blueprint('prompt', __name__)


@REST.resource('/prompt', endpoint='api.prompt.listing')
class PromptListing(CommonListing):
    Model = Prompt
    LISTING_GET = listing_envelope('api.prompt.single')


@REST.resource('/prompt/<slug>', endpoint='api.prompt.single')
class PromptSingle(CommonSingle):
    Model = Prompt
    SINGLE_GET = single_envelope()
