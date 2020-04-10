from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from observatory.forms.extra.validators import SafeSlug
from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


class CommonEditForm(FlaskForm):
    Model = None

    slug = StringField(
        'Slug',
        validators=[DataRequired(), SafeSlug()],
        description='Slug of endpoint',
    )
    title = StringField(
        'Title',
        validators=[DataRequired()],
        description='Title',
    )
    description = TextAreaField(
        'Description',
        description='Description',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.thing = obj

    def validate(self):
        if not super().validate():
            return False

        thing = self.Model.by_slug(self.slug.data)
        if thing is not None:
            if self.thing is None:
                self.slug.errors.append('Already present!')
                return False

            if self.thing.prime != thing.prime:
                self.slug.errors.append('Slug conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.thing:
            self.thing = self.Model.create(slug=self.slug.data, _commit=False)

        self.populate_obj(self.thing)
        return self.thing.save()


class PromptEditForm(CommonEditForm):
    Model = Prompt


class SensorEditForm(CommonEditForm):
    Model = Sensor


class CommonDropForm(FlaskForm):
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
        if not super().validate():
            return False

        return bool(self.thing)

    def action(self):
        if not self.validate():
            return None

        return self.thing.delete()


class PromptDropForm(CommonDropForm):
    Model = Prompt


class SensorDropForm(CommonDropForm):
    Model = Sensor
