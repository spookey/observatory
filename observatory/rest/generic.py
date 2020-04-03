from flask_restful import Resource, abort, marshal
from flask_restful.fields import Boolean, DateTime, String, Url


class MapperSlugUrl(Url):
    def patch(self, obj):
        if self.attribute is not None:
            comm = getattr(obj, self.attribute, None)
            if comm is not None:
                setattr(obj, 'slug', comm.slug)

        for field in ('prompt', 'sensor'):
            elem = getattr(obj, field, None)
            if elem is not None:
                setattr(obj, f'{field}_slug', elem.slug)

        return obj

    def output(self, key, obj):
        return super().output(key, self.patch(obj))


DT_FORMAT = 'iso8601'

COMMON_BASE = {
    'slug': String(),
    'title': String(),
}
MAPPER_BASE = {
    'prompt': String(attribute='prompt.slug'),
    'sensor': String(attribute='sensor.slug'),
    'active': Boolean(),
}


def common_listing(single_ep):
    return dict(
        COMMON_BASE,
        url=Url(endpoint=single_ep, absolute=True),
    )


def common_single(**extra):
    return dict(
        COMMON_BASE,
        description=String(),
        created=DateTime(dt_format=DT_FORMAT),
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
        created=DateTime(dt_format=DT_FORMAT),
        cast=String(attribute='cast.name'),
        color=String(attribute='color.name'),
        horizon=String(attribute='horizon.name'),
        prompt_url=MapperSlugUrl(
            attribute='prompt', endpoint='api.prompt.single', absolute=True,
        ),
        sensor_url=MapperSlugUrl(
            attribute='sensor', endpoint='api.sensor.single', absolute=True,
        ),
    )


class GenericListing(Resource):
    Model = None
    LISTING_GET = None

    def get(self):
        return marshal(self.Model.query.all(), self.LISTING_GET)


class CommonSingle(Resource):
    Model = None
    SINGLE_GET = None

    def common_or_abort(self, slug):
        obj = self.Model.by_slug(slug)
        if not obj:
            abort(404, error=f'{self.Model.__name__} {slug} not present')
        return obj

    def get(self, slug):
        return marshal(self.common_or_abort(slug), self.SINGLE_GET)