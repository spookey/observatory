from flask import Blueprint
from flask_restful import Resource, abort
from flask_restful.fields import Boolean, Float, Integer, String

from observatory.models.mapper import EnumConvert
from observatory.models.prompt import Prompt
from observatory.start.extensions import REST

BP_REST_CHARTS = Blueprint('charts', __name__)


def get_value_step_types(mapper):
    value_type = Float if mapper.convert == EnumConvert.NATURAL else Integer
    step_type = String if mapper.convert == EnumConvert.BOOLEAN else Boolean
    return value_type, step_type


def collect_generic(prompt):
    if prompt.active:
        for mapper in prompt.mapping_active:
            if mapper.active and mapper.sensor and mapper.sensor.active:
                yield mapper, mapper.sensor


def collect_points(mapper, sensor):
    if sensor.active:
        for point in sensor.query_points.all():
            yield dict(
                x=point.created_epoch_ms,
                y=point.convert(mapper.horizon, mapper.convert, numeric=True),
            )


def assemble(prompt):
    for mapper, sensor in collect_generic(prompt):
        points = list(collect_points(mapper, sensor))
        if points:
            value_type, step_type = get_value_step_types(mapper)
            fill, stepped = (
                (False, 'before') if step_type == String else (True, False)
            )
            yield dict(
                borderColor=mapper.color.color,
                data=points,
                fill=fill,
                label=sensor.title,
                steppedLine=stepped,
            ), value_type, step_type


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
