from flask_wtf import FlaskForm
from jinja2 import Markup
from wtforms import SubmitField

from observatory.forms.extra.widgets import SubmitIconInput
from observatory.start.environment import ICON


def test_submiticon_create():
    sii = SubmitIconInput(icon='test')
    assert sii.icon == 'test'


def test_submiticon_ri_icon():
    one = SubmitIconInput(icon='some_thing').ri_icon
    two = SubmitIconInput(icon='user_basic').ri_icon

    for elem in (one, two):
        assert elem.startswith('ri-')
        assert elem.endswith('-line')

    assert ICON['__fallback'] in one
    assert ICON['user_basic'] in two


def test_submiticon_render():
    class PhonyForm(FlaskForm):
        submit = SubmitField(
            'Submit',
            widget=SubmitIconInput(icon='ops_submit'),
        )

    res = PhonyForm().submit()

    assert isinstance(res, Markup)
    assert res.startswith('<button')
    assert ICON['ops_submit'] in res
    assert 'aria-hidden="true"' in res
    assert '<span>Submit</span>' in res
    assert res.endswith('/button>')
