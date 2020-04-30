from flask_wtf import FlaskForm
from wtforms import SubmitField

from observatory.forms.extra.widgets import SubmitButtonInput

# pylint: disable=arguments-differ


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
        return super().validate() and self.thing is not None

    def action(self):
        if not self.validate():
            return None

        return self.thing.delete()


class GenericSortForm(FlaskForm):
    Model = None

    submit = SubmitField(
        'Sort',
        description='Submit',
        widget=SubmitButtonInput(
            icon='glob_error',
            classreplace_kw={'is-dark': 'is-dark is-small'},
        ),
    )

    def __init__(self, *args, obj=None, lift, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.thing = obj
        self.lift = lift

        self.submit.label.text = 'Up' if self.lift else 'Down'
        self.submit.widget.icon = 'ops_arr_up' if self.lift else 'ops_arr_dn'

    def validate(self):
        return (
            super().validate() and
            self.lift is not None and
            bool(self.thing)
        )

    def action(self):
        if not self.validate():
            return None

        if self.lift:
            return self.thing.raise_step()
        return self.thing.lower_step()
