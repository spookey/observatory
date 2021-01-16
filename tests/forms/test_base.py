from flask_wtf import FlaskForm
from pytest import fixture, mark
from wtforms.validators import DataRequired, Optional

from observatory.forms.base import BaseForm
from observatory.forms.extra.widgets import SubmitButtonInput


@fixture(scope='function')
def _field():
    def res(gen, *args, **kwargs):
        class Form(FlaskForm):
            field = gen(*args, **kwargs)

        return Form().field

    yield res


@mark.usefixtures('ctx_app')
class TestBaseForm:
    @staticmethod
    def test_gen_submit_button_empty(_field):
        field = _field(BaseForm.gen_submit_button)

        assert field.label.text == 'Save'
        assert field.description == 'Submit'
        widget = field.widget
        assert isinstance(widget, SubmitButtonInput)
        assert widget.icon == 'ops_submit'
        assert widget.classreplace_kw is None

    @staticmethod
    def test_gen_submit_button(_field):
        label = 'some label'
        description = 'some description'
        icon = 'beautiful'
        classreplace_kw = {'super': 'weird'}

        field = _field(
            BaseForm.gen_submit_button,
            label=label,
            description=description,
            icon=icon,
            classreplace_kw=classreplace_kw,
        )

        assert field.label.text == label
        assert field.description == description
        widget = field.widget
        assert isinstance(widget, SubmitButtonInput)
        assert widget.icon == icon
        assert widget.classreplace_kw == classreplace_kw

    @staticmethod
    def test_gen_select_field_empty(_field):
        label = 'some label'
        description = 'some description'
        coerce = str

        field = _field(
            BaseForm.gen_select_field,
            label,
            coerce=coerce,
            description=description,
        )

        assert field.label.text == label
        assert field.description == description
        assert field.coerce == coerce
        assert field.choices is None
        assert len(field.validators) == 1
        assert all(isinstance(val, DataRequired) for val in field.validators)
        assert field.render_kw is None

    @staticmethod
    def test_gen_select_field(_field):
        label = 'some label'
        description = 'some description'
        coerce = int
        choices = [(1, 'weird'), (2, 'stuff'), (3, 'happy'), (4, 'things')]
        render_kw = {'not': 'shown', 'on': 'page'}

        field = _field(
            BaseForm.gen_select_field,
            label,
            coerce=coerce,
            description=description,
            choices=choices,
            required=False,
            render_kw=render_kw,
        )

        assert field.label.text == label
        assert field.description == description
        assert field.coerce == coerce
        assert field.choices == choices
        assert len(field.validators) == 1
        assert all(isinstance(val, Optional) for val in field.validators)
        assert field.render_kw == render_kw
