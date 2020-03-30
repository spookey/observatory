from pytest import mark
from werkzeug.datastructures import MultiDict

from stats.forms.mapper import MapperEditForm
from stats.models.mapper import (
    EnumAxis, EnumCast, EnumColor, EnumHorizon, Mapper
)

GRAY = 9869462


@mark.usefixtures('session', 'ctx_app')
class TestMapperEditForm:

    @staticmethod
    def test_basic_fields():
        form = MapperEditForm()
        assert form.prompt_sel is not None
        assert form.sensor_sel is not None
        assert form.active is not None
        assert form.axis_sel is not None
        assert form.cast_sel is not None
        assert form.color_sel is not None
        assert form.horizon_sel is not None
        assert form.submit is not None

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
        assert form.axis_sel.choices == [
            (en.value, en.name) for en in EnumAxis
        ]
        assert form.cast_sel.choices == [
            (en.value, en.name) for en in EnumCast
        ]
        assert form.color_sel.choices == [
            (en.value, en.name) for en in EnumColor
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
            axis_sel=1, cast_sel=1,
            color_sel=GRAY, horizon_sel=1,
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
                'axis_sel': 1, 'cast_sel': 1,
                'color_sel': GRAY, 'horizon_sel': 1,
            }),
        )
        assert form.validate() is False
        assert 'combination conflict' in form.prompt_sel.errors[-1].lower()
        assert 'combination conflict' in form.sensor_sel.errors[-1].lower()

    @staticmethod
    def test_edit_existing(gen_prompt, gen_sensor):
        axis = EnumAxis.RIGHT
        cast = EnumCast.BOOLEAN
        color = EnumColor.GRAY
        horizon = EnumHorizon.INVERT

        mapper = Mapper.create(
            prompt=gen_prompt(), sensor=gen_sensor(),
        )
        assert Mapper.query.all() == [mapper]
        form = MapperEditForm(
            obj=mapper, formdata=MultiDict({
                'prompt_sel': mapper.prompt.prime,
                'sensor_sel': mapper.sensor.prime,
                'active': False,
                'axis_sel': axis.value,
                'cast_sel': cast.value,
                'color_sel': color.value,
                'horizon_sel': horizon.value,
            }),
        )
        assert form.validate() is True
        edited = form.action()
        assert edited.prompt == mapper.prompt
        assert edited.sensor == mapper.sensor
        assert edited.active is False
        assert edited.axis == axis
        assert edited.cast == cast
        assert edited.color == color
        assert edited.horizon == horizon

    @staticmethod
    def test_create_new(gen_prompt, gen_sensor):
        prompt = gen_prompt()
        sensor = gen_sensor()
        axis = EnumAxis.LEFT
        cast = EnumCast.INTEGER
        color = EnumColor.TURQUOISE
        horizon = EnumHorizon.NORMAL

        form = MapperEditForm(
            prompt_sel=prompt.prime,
            sensor_sel=sensor.prime,
            active=True,
            axis_sel=axis.value,
            cast_sel=cast.value,
            color_sel=color.value,
            horizon_sel=horizon.value,
        )
        assert form.validate() is True

        mapper = form.action()
        assert mapper.prompt == prompt
        assert mapper.sensor == sensor
        assert mapper.active is True
        assert mapper.axis == axis
        assert mapper.cast == cast
        assert mapper.color == color
        assert mapper.horizon == horizon

        assert Mapper.query.all() == [mapper]
