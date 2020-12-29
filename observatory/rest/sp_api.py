from flask import Blueprint, current_app
from flask_restful import Resource, abort, marshal

from observatory.start.extensions import REST

BP_REST_SP_API = Blueprint('space_api', __name__)


@REST.resource('/space.json', endpoint='api.sp_api.json')
class SpaceApi(Resource):
    @staticmethod
    def get():
        if not current_app.config.get('ENABLE_SP_API', False):
            abort(404)

        return marshal(
            {},
            {},
        )
