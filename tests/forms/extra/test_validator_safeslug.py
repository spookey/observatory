from flask_wtf import FlaskForm
from pytest import mark
from wtforms import StringField

from observatory.forms.extra.validators import SafeSlug

MESSAGE = 'Test Message'


class PhonyForm(FlaskForm):
    slug = StringField('Slug', validators=[SafeSlug(message=MESSAGE)])


@mark.usefixtures('ctx_app')
class TestSafeSlug:
    @staticmethod
    def test_valid():
        form = PhonyForm(slug='x')
        assert form.validate() is True
        assert form.slug.errors == []

    @staticmethod
    def test_invalid():
        form = PhonyForm(slug='🧦')
        assert form.validate() is False
        assert form.slug.errors == [MESSAGE]
