from flask_restful import Resource, abort, marshal
from flask_restful.fields import (
    Boolean,
    DateTime,
    Float,
    Integer,
    Nested,
    String,
    Url,
)


class SlugUrl(Url):
    def patch(self, obj):
        if self.attribute is not None:
            comm = getattr(obj, self.attribute, None)
            if comm is not None:
                setattr(obj, 'slug', comm.slug)

        return obj

    def output(self, key, obj):
        return super().output(key, self.patch(obj))


class MapperSlugUrl(Url):
    @staticmethod
    def patch(obj):
        for field in ('prompt', 'sensor'):
            elem = getattr(obj, field, None)
            if elem is not None:
                setattr(obj, f'{field}_slug', elem.slug)

        return obj

    def output(self, key, obj):
        return super().output(key, self.patch(obj))


DT_FORMAT = 'iso8601'

COMMON_BASE = dict(
    slug=String(),
    title=String(),
)
MAPPER_BASE = dict(
    active=Boolean(),
    prompt=String(attribute='prompt.slug'),
    sensor=String(attribute='sensor.slug'),
)
USER_BASE = dict(
    name=String(attribute='username'),
    active=Boolean(),
)


def common_listing(endpoint):
    return dict(
        COMMON_BASE,
        url=Url(endpoint=endpoint, absolute=True),
    )


def common_single(**extra):
    return dict(
        COMMON_BASE,
        created=DateTime(dt_format=DT_FORMAT),
        description=String(),
        **extra,
    )


def mapper_listing():
    return dict(
        MAPPER_BASE,
        url=MapperSlugUrl(endpoint='api.mapper.single', absolute=True),
    )


def mapper_single():
    return dict(
        MAPPER_BASE,
        color=String(attribute='color.name'),
        convert=String(attribute='convert.name'),
        created=DateTime(dt_format=DT_FORMAT),
        horizon=String(attribute='horizon.name'),
        prompt_url=SlugUrl(
            attribute='prompt',
            endpoint='api.prompt.single',
            absolute=True,
        ),
        sensor_url=SlugUrl(
            attribute='sensor',
            endpoint='api.sensor.single',
            absolute=True,
        ),
        sortkey=Integer(),
    )


def _nest_point(default):
    return Nested(
        default=default,
        nested=dict(
            sensor=String(attribute='sensor.slug'),
            user=String(attribute='user.username'),
            stamp=DateTime(dt_format=DT_FORMAT, attribute='created'),
            value=Float(),
        ),
    )


def sensor_single(nest_name, nest_default):
    res = common_single(
        length=Integer(),
        sticky=Boolean(),
    )
    res[nest_name] = _nest_point(nest_default)
    return res


def user_listing(endpoint):
    return dict(
        USER_BASE,
        url=Url(endpoint=endpoint, absolute=True),
    )


def user_single(nest_name, nest_default):
    res = dict(
        USER_BASE,
        created=DateTime(dt_format=DT_FORMAT),
        last_login=DateTime(dt_format=DT_FORMAT),
        length=Integer(),
    )
    res[nest_name] = _nest_point(nest_default)
    return res


class GenericListing(Resource):
    Model = None
    LISTING_GET = None

    def get(self):
        return marshal(self.Model.query_sorted().all(), self.LISTING_GET), 200


class CommonSingle(Resource):
    Model = None
    SINGLE_GET = None

    def common_or_abort(self, slug):
        obj = self.Model.by_slug(slug)
        if not obj:
            abort(404, message=f'{self.Model.__name__} {slug} not present')
        return obj

    def get(self, slug):
        return marshal(self.common_or_abort(slug), self.SINGLE_GET), 200


class UserSingle(Resource):
    Model = None
    SINGLE_GET = None

    def user_or_abort(self, username):
        obj = self.Model.by_username(username)
        if not obj:
            abort(404, message=f'{self.Model.__name__} {username} not present')
        return obj

    def get(self, username):
        return marshal(self.user_or_abort(username), self.SINGLE_GET), 200
