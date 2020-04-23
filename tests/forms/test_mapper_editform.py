from pytest import mark
from werkzeug.datastructures import MultiDict

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.forms.mapper import MapperEditForm
from observatory.models.mapper import (
    EnumColor, EnumConvert, EnumHorizon, Mapper
)


@mark.usefixtures('session', 'ctx_app')
class TestMapperEditForm:

    @staticmethod
    def test_basic_fields():
        form = MapperEditForm()
        assert form.prompt_sel is not None
        assert form.sensor_sel is not None
        assert form.active is not None
        assert form.color_sel is not None
        assert form.convert_sel is not None
        assert form.horizon_sel is not None
        assert form.elevate is not None
        assert form.submit is not None

    @staticmethod
    def test_submit_button():
        form = MapperEditForm()
        assert form.submit.widget is not None
        assert isinstance(form.submit.widget, SubmitButtonInput)
        assert form.submit.widget.icon == 'ops_submit'

    @staticmethod
    def test_empty_mapper():
        form = MapperEditForm()
        assert form.mapper is None

    @staticmethod
    def test_obj_mapper():
        obj = '💄'
        form = MapperEditForm(obj=obj)
        assert form.mapper == obj

    @staticmethod
    def test_empty_invalid():
        form = MapperEditForm()
        assert form.validate() is False
        assert form.action() is None
        assert form.mapper is None

    @staticmethod
    def test_common_choices(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()
        form = MapperEditForm()

        assert form.prompt_sel.choices == [
            (prompt.prime, f'{prompt.slug} ({prompt.title})')
        ]
        assert form.sensor_sel.choices == [
            (sensor.prime, f'{sensor.slug} ({sensor.title})')
        ]

    @staticmethod
    def test_enum_choices():
        form = MapperEditForm()
        assert form.color_sel.choices == [
            (en.color, en.name) for en in EnumColor
        ]
        assert form.convert_sel.choices == [
            (en.value, en.name) for en in EnumConvert
        ]
        assert form.horizon_sel.choices == [
            (en.value, en.name) for en in EnumHorizon
        ]

    @staticmethod
    def test_commons_unknown():
        form = MapperEditForm(formdata=MultiDict({
            'prompt_sel': 42,
            'sensor_sel': 23,
        }))
        assert form.validate() is False
        assert form.mapper is None

    @staticmethod
    def test_already_present(gen_prompt, gen_sensor):
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        form = MapperEditForm(
            prompt_sel=mapper.prompt.prime,
            sensor_sel=mapper.sensor.prime,
            color_sel=mapper.color.color,
            convert_sel=mapper.convert.value,
            horizon_sel=mapper.horizon.value,
            elevate=mapper.elevate,
        )
        assert form.validate() is False
        assert 'already present' in form.prompt_sel.errors[-1].lower()
        assert 'already present' in form.sensor_sel.errors[-1].lower()

    @staticmethod
    def test_commons_conflict(gen_prompt, gen_sensor):
        orig = Mapper.create(
            prompt=gen_prompt(slug='orig'), sensor=gen_sensor(slug='orig'),
        )
        edit = Mapper.create(
            prompt=gen_prompt(slug='edit'), sensor=gen_sensor(slug='edit'),
        )
        form = MapperEditForm(
            obj=edit, formdata=MultiDict({
                'prompt_sel': orig.prompt.prime,
                'sensor_sel': orig.sensor.prime,
                'color_sel': orig.color.color,
                'convert_sel': orig.horizon.value,
                'horizon_sel': orig.horizon.value,
                'elevate': orig.elevate,
            }),
        )
        assert form.validate() is False
        assert 'combination conflict' in form.prompt_sel.errors[-1].lower()
        assert 'combination conflict' in form.sensor_sel.errors[-1].lower()

    @staticmethod
    def test_edit_existing(gen_prompt, gen_sensor):
        color = EnumColor.ORANGE
        convert = EnumConvert.BOOLEAN
        horizon = EnumHorizon.INVERT
        elevate = 23.42

        mapper = Mapper.create(
            prompt=gen_prompt(), sensor=gen_sensor(),
        )
        assert Mapper.query.all() == [mapper]
        form = MapperEditForm(
            obj=mapper, formdata=MultiDict({
                'prompt_sel': mapper.prompt.prime,
                'sensor_sel': mapper.sensor.prime,
                'active': False,
                'color_sel': color.color,
                'convert_sel': convert.value,
                'horizon_sel': horizon.value,
                'elevate': elevate,
            }),
        )
        assert form.validate() is True
        edited = form.action()
        assert edited.prompt == mapper.prompt
        assert edited.sensor == mapper.sensor
        assert edited.active is False
        assert edited.color == color
        assert edited.convert == convert
        assert edited.horizon == horizon
        assert edited.elevate == elevate

    @staticmethod
    def test_set_selections(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()
        color = EnumColor.BLUE
        convert = EnumConvert.INTEGER
        horizon = EnumHorizon.INVERT

        form = MapperEditForm(obj=Mapper.create(
            prompt=prompt, sensor=sensor,
            color=color, convert=convert, horizon=horizon,
        ))
        assert form.prompt_sel.data != prompt.prime
        assert form.sensor_sel.data != sensor.prime
        assert form.color_sel.data != color.color
        assert form.convert_sel.data != convert.value
        assert form.horizon_sel.data != horizon.value

        form.set_selections()
        assert form.prompt_sel.data == prompt.prime
        assert form.sensor_sel.data == sensor.prime
        assert form.color_sel.data == color.color
        assert form.convert_sel.data == convert.value
        assert form.horizon_sel.data == horizon.value

    @staticmethod
    def test_create_new(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()
        color = EnumColor.TURQUOISE
        convert = EnumConvert.INTEGER
        horizon = EnumHorizon.NORMAL
        elevate = 42.23

        form = MapperEditForm(
            prompt_sel=prompt.prime,
            sensor_sel=sensor.prime,
            active=True,
            color_sel=color.color,
            convert_sel=convert.value,
            horizon_sel=horizon.value,
            elevate=elevate,
        )
        assert form.validate() is True

        mapper = form.action()
        assert mapper.prompt == prompt
        assert mapper.sensor == sensor
        assert mapper.active is True
        assert mapper.color == color
        assert mapper.convert == convert
        assert mapper.horizon == horizon
        assert mapper.elevate == elevate

        assert Mapper.query.all() == [mapper]
