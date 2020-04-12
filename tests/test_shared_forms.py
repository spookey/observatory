from pytest import fixture, mark

from observatory.forms.common import PromptDropForm, SensorDropForm
from observatory.forms.mapper import MapperDropForm, MapperSortForm
from observatory.models.mapper import Mapper
from observatory.shared import (
    form_drop_mapper, form_drop_prompt, form_drop_sensor, form_sort_mapper
)


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _comm(request, gen_prompt, gen_sensor):
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


@mark.usefixtures('session')
class TestSharedForms:

    @staticmethod
    def test_drop_common_empty(_comm):
        form = _comm.func(None)
        assert isinstance(form, _comm.form)
        assert form.thing is None
        assert form.validate() is False

    @staticmethod
    def test_drop_common(_comm):
        thing = _comm.gen_common()
        form = _comm.func(thing)
        assert isinstance(form, _comm.form)
        assert form.thing == thing
        assert form.validate() is True

    @staticmethod
    def test_sort_mapper_empty():
        form = form_sort_mapper(None, None)
        assert isinstance(form, MapperSortForm)
        assert form.mapper is None
        assert form.lift is None
        assert form.validate() is False

    @staticmethod
    def test_sort_mapper(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        form = form_sort_mapper(mapper, True)
        assert isinstance(form, MapperSortForm)
        assert form.mapper == mapper
        assert form.lift is True
        assert form.validate() is True
