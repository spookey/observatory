from pytest import fixture, mark
from werkzeug.datastructures import MultiDict

from observatory.forms.common import PromptEditForm, SensorEditForm
from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.form, res.model, res.gen_common, res.data = (
        (
            PromptEditForm,
            Prompt,
            gen_prompt,
            dict(
                slug='prompt',
                title='The prompt',
                description='Prompt description',
            ),
        )
        if request.param == 'prompt'
        else (
            SensorEditForm,
            Sensor,
            gen_sensor,
            dict(
                slug='sensor',
                title='The sensor',
                description='Sensor description',
                sticky=True,
            ),
        )
    )

    yield res


@mark.usefixtures('session', 'ctx_app')
class TestCommonEditForm:
    @staticmethod
    def test_basic_fields(_comm):
        form = _comm.form()
        assert form.Model == _comm.model
        for key in _comm.data:
            assert getattr(form, key, None) is not None
        assert form.submit is not None

    @staticmethod
    def test_submit_button(_comm):
        form = _comm.form()
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_submit'

    @staticmethod
    def test_empty_thing(_comm):
        form = _comm.form()
        assert form.thing is None

    @staticmethod
    def test_obj_thing(_comm):
        obj = '🦉'
        form = _comm.form(obj=obj)
        assert form.thing == obj

    @staticmethod
    def test_empty_invalid(_comm):
        form = _comm.form()
        assert form.validate() is False
        assert form.action() is None
        assert form.thing is None

    @staticmethod
    def test_no_safe_slug(_comm):
        form = _comm.form(slug='🐭', title='t')
        assert form.validate() is False
        assert 'safe slug' in form.slug.errors[-1].lower()

    @staticmethod
    def test_already_present(_comm):
        thing = _comm.gen_common()
        form = _comm.form(slug=thing.slug, title='t')
        assert form.validate() is False
        assert 'already present' in form.slug.errors[-1].lower()

    @staticmethod
    def test_slug_conflict(_comm):
        orig = _comm.gen_common(slug='original')
        edit = _comm.gen_common(slug='editing')
        form = _comm.form(obj=edit, formdata=MultiDict({'slug': orig.slug}))
        assert form.validate() is False
        assert 'slug conflict' in form.slug.errors[-1].lower()

    @staticmethod
    def test_edit_exisiting(_comm):
        thing = _comm.gen_common()
        assert _comm.model.query.all() == [thing]

        form = SensorEditForm(obj=thing, formdata=MultiDict(_comm.data))
        assert form.validate() is True
        edited = form.action()
        assert edited == thing
        for key, val in _comm.data.items():
            assert getattr(edited, key, 'error') == val
        assert _comm.model.query.all() == [edited]

    @staticmethod
    def test_create_new(_comm):
        form = _comm.form(**_comm.data)
        assert form.validate() is True

        thing = form.action()
        for key, val in _comm.data.items():
            assert getattr(thing, key, 'error') == val

        assert _comm.model.query.all() == [thing]
