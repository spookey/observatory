from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from stats.forms.validators import SafeSlug
from stats.models.sensor import Sensor


class SensorEditForm(FlaskForm):
    slug = StringField(
        'Slug',
        validators=[DataRequired(), SafeSlug()],
        description='Slug of sensor endpoint',
    )
    title = StringField(
        'Title',
        validators=[DataRequired()],
        description='Sensor title',
    )
    description = TextAreaField(
        'Description',
        description='Description',
    )
    submit = SubmitField(
        'Save',
        description='Submit'
    )

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.sensor = obj

    def validate(self):
        if not super().validate():
            return False

        sensor = Sensor.by_slug(self.slug.data)
        if sensor is not None:
            if self.sensor is None:
                self.slug.errors.append('Sensor already present!')
                return False

            if self.sensor.prime != sensor.prime:
                self.slug.errors.append('Sensor slug conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.sensor:
            self.sensor = Sensor.create(slug=self.slug.data, _commit=False)

        self.populate_obj(self.sensor)
        return self.sensor.save()
