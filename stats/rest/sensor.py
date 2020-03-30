from flask import Blueprint
from flask_login import login_required
from flask_restful import fields, marshal
from flask_restful.reqparse import RequestParser

from stats.models.sensor import Sensor
from stats.rest.common import (
    CommonListing, CommonSingle, listing_envelope, single_envelope
)
from stats.start.extensions import REST

BP_REST_SENSOR = Blueprint('sensor', __name__)


@REST.resource('/sensor', endpoint='api.sensor.listing')
class SensorListing(CommonListing):
    Model = Sensor
    LISTING_GET = listing_envelope('api.sensor.single')


@REST.resource('/sensor/<slug>', endpoint='api.sensor.single')
class SensorSingle(CommonSingle):
    Model = Sensor
    SINGLE_GET = single_envelope(
        points=fields.Nested({
            'value': fields.Float(),
            'stamp': fields.DateTime(dt_format='iso8601', attribute='created'),
        })
    )

    @staticmethod
    def parse():
        parser = RequestParser()
        parser.add_argument('value', type=float, required=True)
        return parser.parse_args()

    SINGLE_POST = {
        'slug': fields.String(),
        'uri': fields.Url('api.sensor.single', absolute=True),
    }

    @login_required
    def post(self, slug):
        args = self.parse()
        sensor = self.object_or_abort(slug)
        sensor.append(args.value)
        return marshal(sensor, self.SINGLE_POST), 201
