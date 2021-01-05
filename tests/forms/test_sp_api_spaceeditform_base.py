from random import choice

from pytest import mark
from wtforms import DecimalField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

from observatory.forms.sp_api import SpaceEditForm
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


class PhonyForm(SpaceEditForm):
    KEYS = dict(
        string='test.string',
        number='test.number',
        cstory='test.cstory',
        wrong='checks for wrong access',
    )
    ONE_OF = ['string', 'cstory', 'this_checks_for_wrong_access']

    string = StringField('String')
    number = DecimalField(
        'Number',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=1337)],
    )
    cstory = TextAreaField('Cool story, bro!')


@mark.usefixtures('session', 'ctx_app')
class TestSpaceEditFormBase:
    @staticmethod
    def test_basic_fields():
        idx = choice(range(23, 42))
        form = PhonyForm(idx=idx)
        assert form.string is not None
        assert form.number is not None
        assert form.cstory is not None

        assert getattr(form, 'data', 'error') == dict(
            string=None, number=None, cstory=None
        )

    @staticmethod
    def test_form_idx():
        idx = choice(range(23, 42))
        form = PhonyForm(idx=idx)
        assert form.idx == idx

    @staticmethod
    def test_preloads_data():
        idx = choice(range(23, 42))
        data = dict(
            string=Value.set(
                key=f'{SP_API_PREFIX}.test.string', idx=idx, value='test'
            ).value,
            number=Value.set(
                key=f'{SP_API_PREFIX}.test.number', idx=idx, value=1234.5
            ).value,
            cstory=Value.set(
                key=f'{SP_API_PREFIX}.test.cstory', idx=idx, value='more text'
            ).value,
        )

        form = PhonyForm(idx=idx)
        assert getattr(form, 'data', 'error') == data

    @staticmethod
    def test_validation_fails():
        form = PhonyForm()
        assert form.validate() is False
        assert form.action() is None

        assert ''.join(form.string.errors) == ''
        assert 'required' in ''.join(form.number.errors).lower()
        assert ''.join(form.cstory.errors) == ''

    @staticmethod
    def test_one_of_fails():
        form = PhonyForm(string=None, number=2, cstory=None)
        assert form.validate() is False
        assert form.action() is None

        assert 'at least' in ''.join(form.string.errors).lower()
        assert ''.join(form.number.errors).lower() == ''
        assert 'at least' in ''.join(form.cstory.errors).lower()

    @staticmethod
    def test_action_creates():
        assert Value.query.all() == []

        idx, string, number, cstory = (
            choice(range(23, 42)),
            'text',
            2.5,
            'more test',
        )
        form = PhonyForm(idx=idx, string=string, number=number, cstory=cstory)

        assert form.validate() is True
        assert form.action()

        assert Value.get(key=f'{SP_API_PREFIX}.test.string', idx=idx) == string
        assert Value.get(key=f'{SP_API_PREFIX}.test.number', idx=idx) == number
        assert Value.get(key=f'{SP_API_PREFIX}.test.cstory', idx=idx) == cstory

    @staticmethod
    def test_action_changes():
        idx, string, number, cstory = (
            choice(range(23, 42)),
            None,
            42.0,
            'new story',
        )

        string_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.string', idx=idx, value='old text'
        )
        number_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.number', idx=idx, value=23.5
        )
        cstory_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.cstory', idx=idx, value='good old story'
        )
        assert Value.query.all() == [string_obj, number_obj, cstory_obj]

        form = PhonyForm(idx=idx, string=string, number=number, cstory=cstory)

        assert form.validate() is True
        assert form.action()

        assert Value.get(key=f'{SP_API_PREFIX}.test.string', idx=idx) == string
        assert Value.get(key=f'{SP_API_PREFIX}.test.number', idx=idx) == number
        assert Value.get(key=f'{SP_API_PREFIX}.test.cstory', idx=idx) == cstory
