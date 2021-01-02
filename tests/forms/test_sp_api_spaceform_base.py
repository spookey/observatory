from pytest import mark
from wtforms import DecimalField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

from observatory.forms.sp_api import SpaceForm
from observatory.logic.space_api import PREFIX
from observatory.models.values import Values


class PhonyForm(SpaceForm):
    KEYS = dict(
        string='test.string',
        number='test.number',
        cstory='test.cstory',
        wrong='checks for wrong access',
    )
    ANY_OF = dict(
        number='Number',
        cstory='Story',
        error='checks for wrong access',
    )

    string = StringField('String')
    number = DecimalField(
        'Number',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=1337)],
    )
    cstory = TextAreaField('Cool story, bro!')


@mark.usefixtures('session', 'ctx_app')
class TestSpaceFormBase:
    @staticmethod
    def test_basic_fields():
        idx = 5
        form = PhonyForm(idx=idx)
        assert form.string is not None
        assert form.number is not None
        assert form.cstory is not None

        assert form.idx == idx
        assert getattr(form, 'data', 'error') == dict(
            string=None, number=None, cstory=None
        )

    @staticmethod
    def test_preloads_data():
        idx = 3
        data = dict(
            string=Values.set(
                key=f'{PREFIX}.test.string', idx=idx, value='test'
            ).value,
            number=Values.set(
                key=f'{PREFIX}.test.number', idx=idx, value=1234.5
            ).value,
            cstory=Values.set(
                key=f'{PREFIX}.test.cstory', idx=idx, value='more text'
            ).value,
        )

        form = PhonyForm(idx=idx)
        assert getattr(form, 'data', 'error') == data

    @staticmethod
    def test_form_validation_fails():
        form = PhonyForm()
        assert form.validate() is False
        assert form.action() is None

        assert ''.join(form.string.errors) == ''
        assert 'required' in ''.join(form.number.errors).lower()
        assert ''.join(form.cstory.errors) == ''

    @staticmethod
    def test_form_any_of_fails():
        form = PhonyForm(string=None, number=2, cstory=None)
        assert form.validate() is False
        assert form.action() is None

        assert ''.join(form.string.errors).lower() == ''
        assert 'at least' in ''.join(form.number.errors).lower()
        assert 'at least' in ''.join(form.cstory.errors).lower()

    @staticmethod
    def test_form_action_creates():
        assert Values.query.all() == []

        idx, string, number, cstory = 1, 'text', 2.5, 'more test'
        form = PhonyForm(idx=idx, string=string, number=number, cstory=cstory)

        assert form.validate() is True
        assert form.action()

        assert Values.get(key=f'{PREFIX}.test.string', idx=idx) == string
        assert Values.get(key=f'{PREFIX}.test.number', idx=idx) == number
        assert Values.get(key=f'{PREFIX}.test.cstory', idx=idx) == cstory

    @staticmethod
    def test_form_action_changes():
        idx, string, number, cstory = 2, None, 42.0, 'new story'

        string_obj = Values.set(
            key=f'{PREFIX}.test.string', idx=idx, value='old text'
        )
        number_obj = Values.set(
            key=f'{PREFIX}.test.number', idx=idx, value=23.5
        )
        cstory_obj = Values.set(
            key=f'{PREFIX}.test.cstory', idx=idx, value='good old story'
        )
        assert Values.query.all() == [string_obj, number_obj, cstory_obj]

        form = PhonyForm(idx=idx, string=string, number=number, cstory=cstory)

        assert form.validate() is True
        assert form.action()

        assert Values.get(key=f'{PREFIX}.test.string', idx=idx) == string
        assert Values.get(key=f'{PREFIX}.test.number', idx=idx) == number
        assert Values.get(key=f'{PREFIX}.test.cstory', idx=idx) == cstory
