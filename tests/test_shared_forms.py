from pytest import fixture, mark

from observatory.forms.common import (
    PromptDropForm, PromptSortForm, SensorDropForm, SensorSortForm
)
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.models.mapper import Mapper
from observatory.shared import (
    form_drop_mapper, form_drop_prompt, form_drop_sensor, form_sort_mapper,
    form_sort_prompt, form_sort_sensor
)


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _drop(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.func, res.form, res.gen_common = {
        'prompt': (form_drop_prompt, PromptDropForm, gen_prompt),
        'sensor': (form_drop_sensor, SensorDropForm, gen_sensor),
        'mapper': (
            form_drop_mapper, MapperDropForm,
            lambda: Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        ),
    }.get(request.param)

    yield res


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _sort(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.func, res.form, res.gen_common = {
        'prompt': (form_sort_prompt, PromptSortForm, gen_prompt),
        'sensor': (form_sort_sensor, SensorSortForm, gen_sensor),
        'mapper': (
            form_sort_mapper, MapperSortForm,
            lambda: Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        ),
    }.get(request.param)

    yield res


@mark.usefixtures('session')
class TestSharedForms:

    @staticmethod
    def test_drop_generic_empty(_drop):
        form = _drop.func(None)
        assert isinstance(form, _drop.form)
        assert form.thing is None
        assert form.validate() is False

    @staticmethod
    def test_drop_generic(_drop):
        thing = _drop.gen_common()
        form = _drop.func(thing)
        assert isinstance(form, _drop.form)
        assert form.thing == thing
        assert form.validate() is True

    @staticmethod
    def test_sort_generic_empty(_sort):
        form = _sort.func(None, None)
        assert isinstance(form, _sort.form)
        assert form.thing is None
        assert form.lift is None
        assert form.validate() is False

    @staticmethod
    def test_sort_generic(_sort):
        thing = _sort.gen_common()
        form = _sort.func(thing, True)
        assert isinstance(form, _sort.form)
        assert form.thing == thing
        assert form.lift is True
        assert form.validate() is True
