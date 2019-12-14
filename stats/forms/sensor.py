from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from stats.forms.validators import SafeName
from stats.models.sensor import Sensor


class SensorEditForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), SafeName()],
        description='Name of sensor endpoint',
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

        sensor = Sensor.by_name(self.name.data)
        if sensor is not None:
            if self.sensor is None:
                self.name.errors.append('Sensor already present!')
                return False

            if self.sensor.prime != sensor.prime:
                self.name.errors.append('Sensor name conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.sensor:
            self.sensor = Sensor.create(name=self.name.data, _commit=False)

        self.populate_obj(self.sensor)
        return self.sensor.save()
