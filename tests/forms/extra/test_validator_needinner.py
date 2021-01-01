from random import choice
from string import digits, hexdigits

from flask_wtf import FlaskForm
from wtforms import StringField

from observatory.forms.extra.validators import NeedInner

MESSAGE = 'Test Message'


class PhonyForm(FlaskForm):
    exclusive = StringField(
        'Exclusive',
        validators=[NeedInner(digits, message=MESSAGE, only=True)],
    )
    inclusive = StringField(
        'Inclusive',
        validators=[NeedInner(digits, message=MESSAGE, only=False)],
    )


def test_need_inner_valid():
    form = PhonyForm(
        exclusive=''.join(choice(digits) for _ in range(5)),
        inclusive=''.join(choice(hexdigits) for _ in range(5)),
    )
    assert form.validate() is True
    assert form.exclusive.errors == []
    assert form.inclusive.errors == []


def test_need_start_invalid():
    form = PhonyForm(exclusive='📽', inclusive='🎥')
    assert form.validate() is False
    assert form.exclusive.errors == [MESSAGE]
    assert form.inclusive.errors == [MESSAGE]
