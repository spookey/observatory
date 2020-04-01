from flask import Blueprint
from flask_login import login_required
from flask_restful import marshal
from flask_restful.fields import DateTime, Float, Nested, String, Url
from flask_restful.reqparse import RequestParser

from stats.models.sensor import Sensor
from stats.rest.generic import (
    DT_FORMAT, CommonSingle, GenericListing, common_listing, common_single
)
from stats.start.extensions import REST

BP_REST_SENSOR = Blueprint('sensor', __name__)


@REST.resource('/sensor', endpoint='api.sensor.listing')
class SensorListing(GenericListing):
    Model = Sensor
    LISTING_GET = common_listing('api.sensor.single')


@REST.resource('/sensor/<slug>', endpoint='api.sensor.single')
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
        'url': Url('api.sensor.single', absolute=True),
    }

    @login_required
    def post(self, slug):
        args = self.parse()
        sensor = self.common_or_abort(slug)
        sensor.append(args.value)
        return marshal(sensor, self.SINGLE_POST), 201
