from flask import Blueprint
from flask_login import login_required
from flask_restful import abort, marshal
from flask_restful.fields import DateTime, Float, Nested, String, Url
from flask_restful.reqparse import RequestParser

from observatory.models.sensor import Sensor
from observatory.rest.generic import (
    DT_FORMAT, CommonSingle, GenericListing, common_listing, common_single
)
from observatory.start.extensions import REST

BP_REST_SENSOR = Blueprint('sensor', __name__)


@REST.resource('/sensor', endpoint='api.sensor.listing')
class SensorListing(GenericListing):
    Model = Sensor
    LISTING_GET = common_listing('api.sensor.single')


@REST.resource('/sensor/<string:slug>', endpoint='api.sensor.single')
class SensorSingle(CommonSingle):
    Model = Sensor
    SINGLE_GET = common_single(
        points=Nested({
            'value': Float(),
            'stamp': DateTime(dt_format=DT_FORMAT, attribute='created'),
        })
    )

    @staticmethod
    def parse():
        parser = RequestParser()
        parser.add_argument('value', type=float, required=True)
        return parser.parse_args()

    SINGLE_POST = {
        'slug': String(),
        'url': Url(endpoint='api.sensor.single', absolute=True),
        'value': Float(attribute='latest.value'),
    }

    @login_required
    def post(self, slug):
        args = self.parse()
        sensor = self.common_or_abort(slug)
        if not sensor.append(args.value):
            abort(500, error=f'Could not add {args.value} to {slug}')
        return marshal(sensor, self.SINGLE_POST), 201
