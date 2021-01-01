from random import choice
from string import digits, hexdigits

from flask_wtf import FlaskForm
from wtforms import StringField

from observatory.forms.extra.validators import NeedStart

MESSAGE = 'Test Message'


class PhonyForm(FlaskForm):
    text = StringField(
        'Text', validators=[NeedStart(hexdigits, message=MESSAGE)]
    )


def test_need_start_valid():
    form = PhonyForm(text=''.join(choice(digits) for _ in range(5)))
    assert form.validate() is True
    assert form.text.errors == []


def test_need_start_invalid():
    form = PhonyForm(text='📷')
    assert form.validate() is False
    assert form.text.errors == [MESSAGE]
