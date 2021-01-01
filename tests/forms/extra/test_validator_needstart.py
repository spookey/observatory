from random import choice

from flask_wtf import FlaskForm
from pytest import mark
from wtforms import StringField

from observatory.forms.extra.validators import NeedStart

MESSAGE = 'Test Message'
ST_ONE = '+start'
ST_TWO = '&'


class PhonyForm(FlaskForm):
    one = StringField('one', validators=[NeedStart(ST_ONE, message=MESSAGE)])
    two = StringField('two', validators=[NeedStart(ST_TWO, message=MESSAGE)])
    txt = StringField(
        'txt', validators=[NeedStart(ST_ONE, ST_TWO, message=MESSAGE)]
    )


@mark.usefixtures('ctx_app')
class TestNeedStart:
    @staticmethod
    def test_valid():
        form = PhonyForm(
            one=f'{ST_ONE}abc',
            two=f'{ST_TWO}xyz',
            txt=choice((ST_ONE, ST_TWO)),
        )
        assert form.validate() is True
        assert form.one.errors == []
        assert form.two.errors == []
        assert form.txt.errors == []

    @staticmethod
    def test_invalid():
        form = PhonyForm(one='📷', two='📸', txt='')
        assert form.validate() is False
        assert form.one.errors == [MESSAGE]
        assert form.two.errors == [MESSAGE]
        assert form.txt.errors == [MESSAGE]
