from random import choice

from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.sp_api import SpaceDropForm
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


class PhonyForm(SpaceDropForm):
    KEYS = ['some', 'thing']


@mark.usefixtures('session', 'ctx_app')
class TestSpaceDropFormBase:
    @staticmethod
    def test_basic_fields():
        idx = 5
        form = PhonyForm(idx=idx)
        assert form.submit is not None

    @staticmethod
    def test_form_idx():
        idx = 3
        form = PhonyForm(idx=idx)
        assert form.idx == idx

    @staticmethod
    def test_submit_button():
        idx = choice(range(23, 42))
        form = PhonyForm(idx=idx)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_delete'
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-danger is-small'
        }

    @staticmethod
    def test_validation_fails():
        form = PhonyForm(idx=None)
        assert form.validate() is False
        assert form.action() is None

    @staticmethod
    def test_empty_action():
        form = PhonyForm(idx=23)
        assert form.validate() is True
        assert form.action() is None

    @staticmethod
    def test_delete():
        idx = choice(range(23, 42))
        elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}', idx=idx, value=f'{key} #{idx}'
            )
            for key in PhonyForm.KEYS
        ]

        assert Value.query.all() == elems

        form = PhonyForm(idx=idx)

        assert form.validate() is True
        assert form.action()

        assert Value.query.all() == []

    @staticmethod
    def test_delete_keep_others():
        keep_idx = choice(range(5))
        drop_idx = choice(range(23, 42))
        keep_elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}',
                idx=keep_idx,
                value=f'keep.{key} #{keep_idx}',
            )
            for key in PhonyForm.KEYS
        ]
        drop_elems = [
            Value.set(
                key=f'{SP_API_PREFIX}.{key}',
                idx=drop_idx,
                value=f'drop.{key} #{drop_idx}',
            )
            for key in PhonyForm.KEYS
        ]

        assert Value.query.all() == [*keep_elems, *drop_elems]

        form = PhonyForm(idx=drop_idx)

        assert form.validate() is True
        assert form.action()

        assert Value.query.all() == keep_elems
