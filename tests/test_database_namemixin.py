from pytest import fixture, mark

from stats.database import NameMixin
from stats.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class NameMixinPhony(NameMixin, DB.Model):
    prime = DB.Column(DB.Integer(), primary_key=True)


@fixture(scope='function')
def _nme():
    return NameMixinPhony()


@mark.usefixtures('session')
class TestNameMixin:

    @staticmethod
    def test_tablename(_nme):
        assert _nme.__tablename__ == 'namemixinphony'
