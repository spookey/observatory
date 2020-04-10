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

    res.form, res.model, res.gen_common = (
        PromptEditForm, Prompt, gen_prompt,
    ) if request.param == 'prompt' else (
        SensorEditForm, Sensor, gen_sensor,
    )

    yield res


@mark.usefixtures('session', 'ctx_app')
class TestCommonEditForm:

    @staticmethod
    def test_basic_fields(_comm):
        form = _comm.form()
        assert form.slug is not None
        assert form.title is not None
        assert form.description is not None
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
        form = _comm.form(
            obj=edit, formdata=MultiDict({'slug': orig.slug})
        )
        assert form.validate() is False
        assert 'slug conflict' in form.slug.errors[-1].lower()

    @staticmethod
    def test_edit_exisiting(_comm):
        slug = 'changed_common'
        title = 'The changed common'
        description = 'Some changed common for testing'

        thing = _comm.gen_common()
        assert _comm.model.query.all() == [thing]
        form = SensorEditForm(
            obj=thing, formdata=MultiDict({
                'slug': slug, 'title': title, 'description': description,
            })
        )
        assert form.validate() is True
        edited = form.action()
        assert edited.slug == slug
        assert edited.title == title
        assert edited.description == description
        assert edited == thing
        assert _comm.model.query.all() == [edited]

    @staticmethod
    def test_create_new(_comm):
        slug = 'common'
        title = 'The common'
        description = 'Some common for testing'

        form = _comm.form(slug=slug, title=title, description=description)
        assert form.validate() is True

        thing = form.action()
        assert thing.slug == slug
        assert thing.title == title
        assert thing.description == description

        assert _comm.model.query.all() == [thing]
