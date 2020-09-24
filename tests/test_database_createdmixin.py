from datetime import datetime, timedelta

from pytest import mark

from observatory.database import CreatedMixin, Model
from observatory.start.environment import FMT_STRFTIME

# pylint: disable=too-few-public-methods
# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class CreatedMixinPhony(CreatedMixin, Model):
    pass


@mark.usefixtures('session')
class TestCreatedMixin:
    @staticmethod
    def test_created():
        start = datetime.utcnow()

        crt = CreatedMixinPhony.create(_commit=True)

        assert crt.prime is not None
        assert start <= crt.created
        assert crt.created <= datetime.utcnow()

    @staticmethod
    def test_created_epoch():
        crt = CreatedMixinPhony.create(_commit=True)

        assert (
            crt.created_epoch
            <= (crt.created - datetime.utcfromtimestamp(0)).total_seconds()
        )
        assert crt.created_epoch_ms == 1000 * crt.created_epoch

    @staticmethod
    def test_created_fmt():
        crt = CreatedMixinPhony.create(_commit=True)

        assert crt.created_fmt == crt.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_query_sorted():
        now = datetime.utcnow()
        old = CreatedMixinPhony.create(created=(now + timedelta(days=-1)))
        new = CreatedMixinPhony.create(created=(now + timedelta(days=+1)))

        assert CreatedMixinPhony.query.all() == [old, new]
        assert CreatedMixinPhony.query_sorted().all() == [new, old]
