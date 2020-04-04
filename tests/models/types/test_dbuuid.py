from uuid import uuid4

from pytest import mark, raises
from sqlalchemy.types import BINARY

from observatory.database import Model
from observatory.models.types.dbuuid import DBuuid
from observatory.start.extensions import DB

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class Table(Model):
    uuid = DB.Column(DBuuid(), nullable=True)


@mark.usefixtures('session')
class TestDBUuidOnTable:

    @staticmethod
    def test_set():
        uuid = uuid4()
        model = Table.create()
        assert model.uuid is None
        res = model.update(uuid=uuid)
        assert res.uuid == uuid

    @staticmethod
    def test_get():
        uuid = uuid4()
        model = Table.create(uuid=uuid)
        assert model.uuid == uuid
        res = model.update(uuid=None)
        assert res.uuid is None


class TestDBUuid:

    @staticmethod
    def test_impl():
        assert DBuuid.impl == BINARY

    @staticmethod
    def test_load_dialect():
        def dia():
            pass

        dia.type_descriptor = lambda e: e

        dbuuid = DBuuid()
        dialect = dbuuid.load_dialect(dia)
        assert isinstance(dialect, BINARY)
        assert dialect.length == 16

    @staticmethod
    def test_bind_param():
        dbuuid = DBuuid()
        assert dbuuid.process_bind_param(None, None) is None
        uuid = uuid4()
        assert dbuuid.process_bind_param(uuid, None) == uuid.bytes
        assert dbuuid.process_bind_param(uuid.bytes, None) == uuid.bytes
        assert dbuuid.process_bind_param(uuid.int, None) == uuid.bytes
        assert dbuuid.process_bind_param(uuid.hex, None) == uuid.bytes
        with raises(ValueError):
            dbuuid.process_bind_param(float('inf'), None)
        with raises(ValueError):
            dbuuid.process_bind_param('🍦', None)

    @staticmethod
    def test_result_value():
        dbuuid = DBuuid()
        assert dbuuid.process_result_value(None, None) is None
        uuid = uuid4()
        assert dbuuid.process_result_value(uuid, None) == uuid
        assert dbuuid.process_result_value(uuid.bytes, None) == uuid
