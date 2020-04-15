from pytest import mark

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.mapper import MapperSortForm
from observatory.models.mapper import Mapper


@mark.usefixtures('session', 'ctx_app')
class TestMapperSortForm:

    @staticmethod
    @mark.parametrize('lift', [True, False])
    def test_basic_fields(lift):
        form = MapperSortForm(lift=lift)
        assert form.submit is not None

    @staticmethod
    @mark.parametrize('_lift_text', [
        (True, 'Up'), (False, 'Down')
    ])
    def test_submit_label(_lift_text):
        lift, text = _lift_text
        form = MapperSortForm(lift=lift)
        assert form.submit.label is not None
        assert form.submit.label.text == text

    @staticmethod
    @mark.parametrize('_lift_icon', [
        (True, 'ops_arr_up'), (False, 'ops_arr_dn')
    ])
    def test_submit_icon(_lift_icon):
        lift, icon = _lift_icon
        form = MapperSortForm(lift=lift)
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == icon
        assert form.submit.widget.classreplace_kw == {
            'is-dark': 'is-dark is-small'
        }

    @staticmethod
    def test_empty_mapper_and_lift():
        form = MapperSortForm(lift=None)
        assert form.thing is None
        assert form.lift is None

    @staticmethod
    def test_obj_mapper():
        obj = '🕊'
        form = MapperSortForm(obj=obj, lift=None)
        assert form.thing == obj

    @staticmethod
    def test_empty_invalid():
        form = MapperSortForm(lift=None)
        assert form.validate() is False
        assert form.action() is None
        assert form.thing is None

    @staticmethod
    def test_sort(gen_prompt, gen_sensor):
        one = Mapper.create(
            prompt=gen_prompt('one'), sensor=gen_sensor('one'), sortkey=1
        )
        two = Mapper.create(
            prompt=gen_prompt('two'), sensor=gen_sensor('two'), sortkey=2
        )

        def _order(obj, lift, act=True):
            form = MapperSortForm(obj=obj, lift=lift)
            assert form.validate() is True
            assert form.action() == act

            return Mapper.query_sorted().all()

        assert Mapper.query_sorted().all() == [two, one]

        assert _order(one, True) == [one, two]
        assert _order(one, False) == [two, one]
        assert _order(two, False) == [one, two]
        assert _order(two, True) == [two, one]

        assert _order(two, True, act=False) == [two, one]
        assert _order(one, False, act=False) == [two, one]
