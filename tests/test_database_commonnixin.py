from pytest import mark

from observatory.database import CommonMixin, Model

# pylint: disable=too-few-public-methods
# pylint: disable=no-member
# pylint: disable=too-many-ancestors

SLUG = 'test'
TITLE = 'Test title'
DESCRIPTION = 'Description of test'


class CommonMixinPhony(CommonMixin, Model):
    pass


@mark.usefixtures('session')
class TestCommonMixin:

    @staticmethod
    def test_fields():
        cmn = CommonMixinPhony.create(
            slug=SLUG, title=TITLE, description=DESCRIPTION
        )

        assert cmn.slug == SLUG
        assert cmn.title == TITLE
        assert cmn.description == DESCRIPTION

    @staticmethod
    def test_by_slug():
        cmn = CommonMixinPhony.create(
            slug=SLUG, title=TITLE, description=DESCRIPTION
        )

        assert CommonMixinPhony.query.all() == [cmn]

        assert CommonMixinPhony.by_slug(SLUG) == cmn
