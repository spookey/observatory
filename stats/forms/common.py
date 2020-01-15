from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from stats.forms.validators import SafeSlug
from stats.models.prompt import Prompt
from stats.models.sensor import Sensor


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


class SensorEditForm(CommonEditForm):
    Model = Sensor


class PromptEditForm(CommonEditForm):
    Model = Prompt
