from flask_wtf import FlaskForm
from wtforms import StringField

from observatory.forms.extra.validators import SafeSlug

MESSAGE = 'Test Message'


class PhonyForm(FlaskForm):
    slug = StringField('Slug', validators=[SafeSlug(message=MESSAGE)])


def test_safe_slug_valid():
    form = PhonyForm(slug='x')
    assert form.validate() is True
    assert form.slug.errors == []


def test_safe_slug_invalid():
    form = PhonyForm(slug='🧦')
    assert form.validate() is False
    assert form.slug.errors == [MESSAGE]
