from pytest import mark

from stats.database import NameMixin
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class NameMixinPhony(NameMixin, DB.Model):
    prime = DB.Column(DB.Integer(), primary_key=True)


@mark.usefixtures('session')
class TestNameMixin:

    @staticmethod
    def test_tablename():
        nme = NameMixinPhony()

        assert nme.__tablename__ == 'namemixinphony'
