from pytest import mark

from observatory.database import TXT_LEN_SHORT, CRUDMixin
from observatory.start.extensions import DB

# pylint: disable=no-member

PAYLOAD = 'omg wtf bbq'
LAYPOAD = 'napfkuchen!'


class CRUDMixinPhony(CRUDMixin, DB.Model):
    prime = DB.Column(DB.Integer(), primary_key=True)
    value = DB.Column(DB.String(length=TXT_LEN_SHORT))


@mark.usefixtures('session')
class TestCRUDMixin:
    @staticmethod
    def test_create_no_commit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=False)

        assert crud.prime is None
        assert crud.value == PAYLOAD
        assert crud in CRUDMixinPhony.query.all()

    @staticmethod
    def test_create_commit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=True)

        assert crud.prime == 1
        assert crud.value == PAYLOAD
        assert crud in CRUDMixinPhony.query.all()

    @staticmethod
    def test_update_no_comit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=False)

        assert crud.value == PAYLOAD
        crud.update(value=LAYPOAD, _commit=False)
        assert crud.value == LAYPOAD

    @staticmethod
    def test_update_comit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=True)

        assert crud.value == PAYLOAD
        crud.update(value=LAYPOAD, _commit=True)
        assert crud.value == LAYPOAD

    @staticmethod
    def test_save_no_commit(session):
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=False)

        assert crud not in session.dirty
        crud.value = LAYPOAD
        assert crud not in session.dirty
        crud.save(_commit=False)
        assert crud not in session.dirty

    @staticmethod
    def test_save_commit(session):
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=True)

        assert crud not in session.dirty
        crud.value = LAYPOAD
        assert crud in session.dirty
        crud.save(_commit=True)
        assert crud not in session.dirty

    @staticmethod
    def test_delete_no_commit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=False)

        assert crud in CRUDMixinPhony.query.all()
        crud.delete(_commit=False)
        assert crud not in CRUDMixinPhony.query.all()

    @staticmethod
    def test_delete_commit():
        crud = CRUDMixinPhony.create(value=PAYLOAD, _commit=True)

        assert crud in CRUDMixinPhony.query.all()
        crud.delete(_commit=True)
        assert crud not in CRUDMixinPhony.query.all()

    @staticmethod
    def test_logging(caplog):
        crud = CRUDMixinPhony.create(value='yes', _commit=True)

        log_c, log_s = caplog.records[-2:]
        assert 'creating' in log_c.message.lower()
        assert 'saving' in log_s.message.lower()

        crud.update(value='no')
        log_u, log_s = caplog.records[-2:]
        assert 'updating' in log_u.message.lower()
        assert 'saving' in log_s.message.lower()

        crud.delete()
        log_d = caplog.records[-1]
        assert 'deleting' in log_d.message.lower()
