from flask_wtf import FlaskForm
from pytest import mark
from wtforms import StringField

from observatory.forms.extra.validators import NeedInner

MESSAGE = 'Test Message'
PATTERN = 'abc'


class PhonyForm(FlaskForm):
    exclusive = StringField(
        'Exclusive',
        validators=[NeedInner(PATTERN, message=MESSAGE, only=True)],
    )
    inclusive = StringField(
        'Inclusive',
        validators=[NeedInner(PATTERN, message=MESSAGE, only=False)],
    )


@mark.usefixtures('ctx_app')
class TestNeedInner:
    @staticmethod
    def test_valid():
        form = PhonyForm(
            exclusive=''.join('acab'),
            inclusive=''.join('abcd'),
        )
        assert form.validate() is True
        assert form.exclusive.errors == []
        assert form.inclusive.errors == []

    @staticmethod
    def test_invalid():
        form = PhonyForm(exclusive='📽', inclusive='🎥')
        assert form.validate() is False
        assert form.exclusive.errors == [MESSAGE]
        assert form.inclusive.errors == [MESSAGE]
