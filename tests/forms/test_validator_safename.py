from flask_wtf import FlaskForm
from wtforms import StringField

from stats.forms.validators import SafeName

MESSAGE = 'Test Mesasge'


class PhonyForm(FlaskForm):
    name = StringField('Name', validators=[SafeName(message=MESSAGE)])


def test_safe_name_valid():
    form = PhonyForm(name='x')
    assert form.validate() is True
    assert form.name.errors == []


def test_safe_name_invalid():
    form = PhonyForm(name='🧦')
    assert form.validate() is False
    assert form.name.errors == [MESSAGE]
