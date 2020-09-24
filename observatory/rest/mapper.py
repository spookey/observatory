from flask import Blueprint
from flask_restful import Resource, abort, marshal

from observatory.models.mapper import Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor
from observatory.rest.generic import (
    GenericListing,
    mapper_listing,
    mapper_single,
)
from observatory.start.extensions import REST

BP_REST_MAPPER = Blueprint('mapper', __name__)


@REST.resource('/mapper', endpoint='api.mapper.listing')
class MapperListing(GenericListing):
    Model = Mapper
    LISTING_GET = mapper_listing()


@REST.resource(
    '/mapper/prompt/<string:prompt_slug>/sensor/<string:sensor_slug>',
    '/mapper/sensor/<string:sensor_slug>/prompt/<string:prompt_slug>',
    endpoint='api.mapper.single',
)
class MapperSingle(Resource):
    SINGLE_GET = mapper_single()

    @staticmethod
    def object_or_abort(prompt_slug, sensor_slug):
        obj = Mapper.by_commons(
            prompt=Prompt.by_slug(prompt_slug),
            sensor=Sensor.by_slug(sensor_slug),
        )
        if not obj:
            abort(
                404, message=f'Mapper {prompt_slug} {sensor_slug} not present'
            )
        return obj

    def get(self, prompt_slug, sensor_slug):
        return marshal(
            self.object_or_abort(prompt_slug, sensor_slug),
            self.SINGLE_GET
        ), 200
