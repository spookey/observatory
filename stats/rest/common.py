from flask_restful import Resource, abort, fields, marshal

BASE_ENVELOPE = {
    'slug': fields.String(),
    'title': fields.String(),
    'description': fields.String(),
    'created': fields.DateTime(dt_format='iso8601'),
}


def listing_envelope(single_ep):
    return dict(
        BASE_ENVELOPE,
        single=fields.Url(endpoint=single_ep, absolute=True)
    )


def single_envelope(**extra):
    return dict(
        BASE_ENVELOPE,
        **extra
    )


class CommonListing(Resource):
    Model = None
    LISTING_GET = None

    def get(self):
        return marshal(self.Model.query.all(), self.LISTING_GET)


class CommonSingle(Resource):
    Model = None
    SINGLE_GET = None

    def object_or_abort(self, slug):
        obj = self.Model.by_slug(slug)
        if not obj:
            abort(404, error=f'{self.Model.__name__} {slug} not present')
        return obj

    def get(self, slug):
        return marshal(self.object_or_abort(slug), self.SINGLE_GET)
