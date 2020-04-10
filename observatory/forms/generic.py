from flask_wtf import FlaskForm
from wtforms import SubmitField

from observatory.forms.extra.widgets import SubmitButtonInput


class GenericDropForm(FlaskForm):
    Model = None

    submit = SubmitField(
        'Delete',
        description='Submit',
        widget=SubmitButtonInput(
            icon='ops_delete',
            classreplace_kw={'is-dark': 'is-danger is-small'},
        ),
    )

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.thing = obj

    def validate(self):
        return super().validate() and bool(self.thing)

    def action(self):
        if not self.validate():
            return None

        return self.thing.delete()
