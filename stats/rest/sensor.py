from flask import Blueprint
from flask_login import login_required
from flask_restful import Resource, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser

from stats.models.sensor import Sensor
from stats.start.extensions import REST

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

BP_REST_SENSOR = Blueprint('sensor', __name__)


@REST.resource('/sensor', endpoint='api.sensor.listing')
class SensorListing(Resource):

    LISTING_GET = {
        'name': fields.String(),
        'title': fields.String(),
        'description': fields.String(),
        'created': fields.DateTime(dt_format='iso8601'),
    }

    @marshal_with(LISTING_GET)
    def get(self):
        return Sensor.query.all()


@REST.resource('/sensor/<name>', endpoint='api.sensor.single')
class SensorSingle(Resource):

    SINGLE_GET = {
        'name': fields.String(),
        'points': fields.Nested({
            'value': fields.Float(),
            'stamp': fields.DateTime(dt_format='iso8601'),
        }),
    }

    @staticmethod
    def sensor_or_abort(name):
        sensor = Sensor.by_name(name)
        if not sensor:
            abort(404, message=f'Sensor {name} not present')
        return sensor

    @marshal_with(SINGLE_GET)
    def get(self, name):
        return self.sensor_or_abort(name)

    @staticmethod
    def parse():
        parser = RequestParser()
        parser.add_argument('value', type=float, required=True)
        return parser.parse_args()

    SINGLE_POST = {
        'name': fields.String(),
        'uri': fields.Url('api.sensor.single', absolute=True),
    }

    @login_required
    @marshal_with(SINGLE_POST)
    def post(self, name):
        args = self.parse()
        sensor = self.sensor_or_abort(name)
        sensor.append(args.value)
        return sensor, 201
