from flask import Blueprint
from flask_restful import Resource, abort, marshal
from flask_restful.fields import Boolean, Float, Integer, List, Nested, String

from observatory.models.mapper import EnumConvert
from observatory.models.prompt import Prompt
from observatory.start.extensions import REST

BP_REST_CHARTS = Blueprint('charts', __name__)


def dataset(value_type, step_type):
    return dict(
        borderColor=String(default=None),
        data=List(
            Nested(
                default={},
                nested=dict(
                    x=Integer(default=0),
                    y=value_type(default=0),
                ),
            )
        ),
        display=Nested(
            default={},
            nested=dict(
                logic=Nested(
                    default={},
                    nested=dict(
                        color=String(default=''),
                        epoch=Integer(default=0),
                        stamp=String(default=''),
                    ),
                ),
                plain=Nested(
                    default={},
                    nested=dict(
                        convert=String(default=''),
                        description=String(default=''),
                        horizon=String(default=''),
                        points=Integer(default=0),
                        slug=String(default=''),
                        title=String(default=''),
                        value=String(default=''),
                    ),
                ),
            ),
        ),
        fill=Boolean(default=True),
        label=String(default=''),
        lineTension=Float(default=0.4),
        steppedLine=step_type(default=False),
    )


def get_value_step_types(mapper):
    value_type = Integer if mapper.convert == EnumConvert.INTEGER else Float
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
                y=point.translate_map(mapper, numeric=True),
            )


def assemble(prompt):
    for mapper, sensor in collect_generic(prompt):
        points = list(collect_points(mapper, sensor))
        if points and sensor.latest:
            value_type, step_type = get_value_step_types(mapper)

            fill, stepped = True, False
            if mapper.convert == EnumConvert.BOOLEAN:
                fill, stepped = False, 'before'
            tension = 0.4
            if mapper.convert == EnumConvert.INTEGER:
                tension = 0.0

            yield dict(
                borderColor=mapper.color.color,
                data=points,
                display=dict(
                    logic=dict(
                        color=mapper.color.color,
                        epoch=sensor.latest.created_epoch_ms,
                        stamp=sensor.latest.created_fmt,
                    ),
                    plain=dict(
                        convert=mapper.convert.name,
                        description=sensor.description,
                        horizon=mapper.horizon.name,
                        points=len(points),
                        slug=sensor.slug,
                        title=sensor.title,
                        value=sensor.latest.translate_map(mapper),
                    ),
                ),
                fill=fill,
                label=sensor.title,
                lineTension=tension,
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

        return [
            marshal(payload, dataset(value_type, step_type))
            for payload, value_type, step_type in assemble(prompt)
        ], 200
