from pytest import fixture, mark

from observatory.forms.common import PromptDropForm, SensorDropForm
from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.mapper import MapperDropForm
from observatory.models.mapper import Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.form, res.model, res.gen_common = {
        'prompt': (PromptDropForm, Prompt, gen_prompt),
        'sensor': (SensorDropForm, Sensor, gen_sensor),
        'mapper': (
            MapperDropForm, Mapper,
            lambda: Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        ),
    }.get(request.param)

    yield res


@mark.usefixtures('session', 'ctx_app')
class TestGenericDropForm:

    @staticmethod
    def test_basic_fields(_comm):
        form = _comm.form()
        assert form.Model == _comm.model
        assert form.submit is not None

    @staticmethod
    def test_submit_icon(_comm):
        form = _comm.form()
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_delete'
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-danger is-small'
        }

    @staticmethod
    def test_empty_thing(_comm):
        form = _comm.form()
        assert form.thing is None

    @staticmethod
    def test_obj_thing(_comm):
        obj = '🦃'
        form = _comm.form(obj=obj)
        assert form.thing == obj

    @staticmethod
    def test_empty_invalid(_comm):
        form = _comm.form()
        assert form.validate() is False
        assert form.action() is None
        assert form.thing is None

    @staticmethod
    def test_delete(_comm):
        thing = _comm.gen_common()
        assert _comm.model.query.all() == [thing]

        form = _comm.form(obj=thing)
        assert form.validate() is True
        assert form.action() is True

        assert _comm.model.query.all() == []
