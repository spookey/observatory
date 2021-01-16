from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

from observatory.forms.extra.widgets import SubmitButtonInput


class BaseForm(FlaskForm):
    @staticmethod
    def gen_submit_button(
        label='Save',
        *,
        description='Submit',
        icon='ops_submit',
        classreplace_kw=None,
    ):
        return SubmitField(
            label,
            description=description,
            widget=SubmitButtonInput(icon, classreplace_kw=classreplace_kw),
        )

    @staticmethod
    def gen_select_field(
        label,
        *,
        description,
        coerce,
        choices=None,
        required=True,
        render_kw=None,
    ):
        return SelectField(
            label,
            description=description,
            coerce=coerce,
            choices=choices,
            validators=[DataRequired()] if required else [Optional()],
            render_kw=render_kw,
        )
