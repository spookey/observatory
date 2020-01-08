from pytest import mark

from stats.database import CommonMixin, Model

# pylint: disable=too-few-public-methods
# pylint: disable=no-member
# pylint: disable=too-many-ancestors

NAME = 'test'
TITLE = 'Test title'
DESCRIPTION = 'Description of test'


class CommonMixinPhony(CommonMixin, Model):
    pass


@mark.usefixtures('session')
class TestCommonMixin:

    @staticmethod
    def test_fields():
        cmn = CommonMixinPhony.create(
            name=NAME, title=TITLE, description=DESCRIPTION
        )

        assert cmn.name == NAME
        assert cmn.title == TITLE
        assert cmn.description == DESCRIPTION

    @staticmethod
    def test_by_name():
        cmn = CommonMixinPhony.create(
            name=NAME, title=TITLE, description=DESCRIPTION
        )

        assert CommonMixinPhony.query.all() == [cmn]

        assert CommonMixinPhony.by_name(NAME) == cmn
