from flask_wtf import FlaskForm
from markupsafe import Markup
from pytest import mark
from wtforms import SubmitField

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.start.environment import ICON


@mark.usefixtures('ctx_app')
class TestSubmitButtonInput:
    @staticmethod
    def test_init():
        sbi = SubmitButtonInput(icon='some', classreplace_kw={'what': 'ever'})
        assert sbi.input_type == 'submit'
        assert sbi.icon == 'some'
        assert sbi.classreplace_kw == {'what': 'ever'}

    @staticmethod
    def test_render():
        def fld():
            pass

        field = fld
        field.label = fld
        field.id = 'some-id'
        field.name = 'Some name'
        field.label.text = 'Some text'

        res = SubmitButtonInput()(field)
        assert isinstance(res, Markup)

        assert res.startswith('<button')
        assert res.endswith('button>')

        assert 'type="submit"' in res
        assert f'id="{field.id}"' in res
        assert f'name="{field.name}"' in res
        assert f'value="{field.label.text}"' in res
        assert f'<span>{field.label.text}</span>' in res

    @staticmethod
    def test_form():
        icon = 'ops_submit'
        class_ = 'something'
        class_drop = 'is-wrong'
        class_add = 'is-fine'

        class PhonyForm(FlaskForm):
            submit = SubmitField(
                'Submit',
                widget=SubmitButtonInput(
                    icon=icon, classreplace_kw={class_drop: class_add}
                ),
                render_kw={'class_': f'{class_} {class_drop}'},
            )

        res = PhonyForm().submit()
        assert isinstance(res, Markup)

        assert res.startswith('<button')
        assert res.endswith('button>')

        assert 'type="submit"' in res
        assert 'id="submit"' in res
        assert 'name="submit"' in res
        assert 'value="Submit"' in res
        assert '<span>Submit</span>' in res

        assert f'class="{class_} {class_add}"' in res

        assert 'class="icon"' in res
        assert f'class="ri-{ICON[icon]}-line"' in res
