from pytest import mark

from observatory.database import PrimeMixin
from observatory.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class PrimeMixinPhony(PrimeMixin, DB.Model):
    pass


@mark.usefixtures('session')
class TestPrimeMixin:
    @staticmethod
    def test_primekey_init():
        pri = PrimeMixinPhony()

        assert pri is not None
        assert pri.prime is None

    @staticmethod
    def test_primekey_autoset(session):
        one = PrimeMixinPhony()
        two = PrimeMixinPhony()
        session.add_all((one, two))
        session.commit()
        assert one.prime == 1
        assert two.prime == 2

    @staticmethod
    def test_by_prime_not_found():
        res = PrimeMixinPhony.by_prime(1337)
        assert res is None

    @staticmethod
    def test_by_prime(session):
        pri = PrimeMixinPhony()

        session.add(pri)
        session.commit()
        assert pri == PrimeMixinPhony.by_prime(1)

    @staticmethod
    def test_by_prime_types(session):
        pri = PrimeMixinPhony()

        session.add(pri)
        session.commit()
        assert pri == PrimeMixinPhony.by_prime(1)
        assert pri == PrimeMixinPhony.by_prime(1.0)
        assert pri == PrimeMixinPhony.by_prime('1')
        assert pri == PrimeMixinPhony.by_prime(b'1')

    @staticmethod
    def test_by_prime_invalid(session):
        pri = PrimeMixinPhony()

        session.add(pri)
        session.commit()
        assert pri == PrimeMixinPhony.by_prime(1)
        assert None is PrimeMixinPhony.by_prime(-1)
        assert None is PrimeMixinPhony.by_prime(0.1)
        assert None is PrimeMixinPhony.by_prime(0.9)
        assert None is PrimeMixinPhony.by_prime('omg')
        assert None is PrimeMixinPhony.by_prime(b'wtf')
        assert None is PrimeMixinPhony.by_prime('🤷‍♀️')
