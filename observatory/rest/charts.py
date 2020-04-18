from flask import Blueprint
from flask_restful import Resource, abort

from observatory.models.prompt import Prompt
from observatory.start.extensions import REST

BP_REST_CHARTS = Blueprint('charts', __name__)


@REST.resource('/charts/<string:slug>', endpoint='api.charts.plot')
class ChartsPlot(Resource):

    @staticmethod
    def prompt_active_or_abort(slug):
        prompt = Prompt.by_slug(slug)
        if not prompt:
            abort(404, message=f'Prompt {slug} not present')
        if not prompt.active:
            abort(410, message=f'Prompt {slug} not active')
        return prompt

    def get(self, slug):
        prompt = self.prompt_active_or_abort(slug)

        return dict(
            todo=f'output plot data for {prompt.slug}',
        ), 200
