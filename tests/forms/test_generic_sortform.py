from pytest import fixture, mark

from observatory.forms.common import PromptSortForm, SensorSortForm
from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.mapper import MapperSortForm
from observatory.models.mapper import Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.form, res.model, res.gen_generic = {
        'prompt': (PromptSortForm, Prompt, gen_prompt),
        'sensor': (SensorSortForm, Sensor, gen_sensor),
        'mapper': (
            MapperSortForm,
            Mapper,
            lambda slug='test': Mapper.create(
                prompt=gen_prompt(slug=f'm_{slug}'),
                sensor=gen_sensor(slug=f'm_{slug}'),
            ),
        ),
    }.get(request.param)

    yield res


@mark.usefixtures('session', 'ctx_app')
class TestGenericSortForm:
    @staticmethod
    @mark.parametrize('lift', [True, False])
    def test_basic_fields(_comm, lift):
        form = _comm.form(lift=lift)
        assert form.Model == _comm.model
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('_lift_text', [(True, 'Up'), (False, 'Down')])
    def test_submit_label(_comm, _lift_text):
        lift, text = _lift_text
        form = _comm.form(lift=lift)
        assert form.submit.label is not None
        assert form.submit.label.text == text

    @staticmethod
    @mark.parametrize(
        '_lift_icon', [(True, 'ops_arr_up'), (False, 'ops_arr_dn')]
    )
    def test_submit_icon(_comm, _lift_icon):
        lift, icon = _lift_icon
        form = _comm.form(lift=lift)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == icon
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-dark is-small'
        }

    @staticmethod
    def test_empty_mapper_and_lift(_comm):
        form = _comm.form(lift=None)
        assert form.thing is None
        assert form.lift is None

    @staticmethod
    def test_obj_mapper(_comm):
        obj = '🕊'
        form = _comm.form(obj=obj, lift=None)
        assert form.thing == obj

    @staticmethod
    def test_empty_invalid(_comm):
        form = _comm.form(lift=None)
        assert form.validate() is False
        assert form.action() is None
        assert form.thing is None

    @staticmethod
    def test_sort(_comm):
        one = _comm.gen_generic('one')
        two = _comm.gen_generic('two')

        def _order(obj, lift, act=True):
            form = _comm.form(obj=obj, lift=lift)
            assert form.validate() is True
            assert form.action() == act

            return _comm.model.query_sorted().all()

        assert _comm.model.query_sorted().all() == [two, one]

        assert _order(one, True) == [one, two]
        assert _order(one, False) == [two, one]
        assert _order(two, False) == [one, two]
        assert _order(two, True) == [two, one]

        assert _order(two, True, act=False) == [two, one]
        assert _order(one, False, act=False) == [two, one]
