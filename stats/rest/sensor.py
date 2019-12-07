from flask import Blueprint
from flask_restful import Resource, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser

from stats.models.point import Point
from stats.models.sensor import Sensor
from stats.start.extensions import REST

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use

BP_REST_SENSOR = Blueprint('sensor', __name__)


@REST.resource('/sensor', endpoint='api.sensor.listing')
class SensorListing(Resource):

    LISTING = {
        'name': fields.String(),
        'title': fields.String(),
        'description': fields.String(),
        'created': fields.DateTime(dt_format='iso8601'),
    }

    @marshal_with(LISTING)
    def get(self):
        return Sensor.query.all()


@REST.resource('/sensor/<name>', endpoint='api.sensor.single')
class SensorSingle(Resource):

    SINGLE = {
        'name': fields.String(),
        'points': fields.Nested({
            'value': fields.Float(),
            'stamp': fields.DateTime(dt_format='iso8601'),
        }),
    }

    @staticmethod
    def get_or_abort(name):
        sensor = Sensor.by_name(name)
        if not sensor:
            abort(404, message='Sensor {} not present'.format(name))
        return sensor

    @marshal_with(SINGLE)
    def get(self, name):
        return self.get_or_abort(name)

    @staticmethod
    def parse():
        parser = RequestParser()
        parser.add_argument('value', type=float, required=True)
        return parser.parse_args()

    @marshal_with(SINGLE)
    def post(self, name):
        args = self.parse()
        sensor = self.get_or_abort(name)
        Point.create(sensor=sensor, value=args.value)
        return sensor
