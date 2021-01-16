from wtforms import BooleanField, DecimalField
from wtforms.validators import NumberRange

from observatory.forms.base import BaseForm
from observatory.forms.generic import GenericDropForm, GenericSortForm
from observatory.models.mapper import (
    EnumColor,
    EnumConvert,
    EnumHorizon,
    Mapper,
)
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor

# pylint: disable=arguments-differ
# pylint: disable=no-member


class MapperEditForm(BaseForm):
    prompt_sel = BaseForm.gen_select_field(
        'Prompt', description='Select prompt', coerce=int
    )
    sensor_sel = BaseForm.gen_select_field(
        'Sensor', description='Select sensor', coerce=int
    )
    active = BooleanField(
        'Active',
        default=True,
        description='Set active',
    )
    elevate = DecimalField(
        'Elevate',
        default=1.0,
        places=4,
        validators=[NumberRange(min=0.0)],
        description='Increase raw value with this factor',
    )
    color_sel = BaseForm.gen_select_field(
        'Color',
        description='Select color',
        coerce=str,
        choices=[(en.color, en.name) for en in EnumColor],
        render_kw={'data_colorize': 'option'},
    )
    convert_sel = BaseForm.gen_select_field(
        'Convert',
        description='Select conversion',
        coerce=int,
        choices=[(en.value, en.name) for en in EnumConvert],
    )
    horizon_sel = BaseForm.gen_select_field(
        'Horizon',
        description='Select horizon',
        coerce=int,
        choices=[(en.value, en.name) for en in EnumHorizon],
    )
    submit = BaseForm.gen_submit_button()

    @staticmethod
    def _comm_choices(model):
        return [
            (cm.prime, f'{cm.slug} ({cm.title})')
            for cm in model.query.order_by('slug').all()
        ]

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.mapper = obj

        self.prompt_sel.choices = self._comm_choices(Prompt)
        self.sensor_sel.choices = self._comm_choices(Sensor)

    def set_selections(self):
        if not self.mapper:
            return
        self.prompt_sel.data = self.mapper.prompt_prime
        self.sensor_sel.data = self.mapper.sensor_prime

        self.color_sel.data = self.mapper.color.color
        self.convert_sel.data = self.mapper.convert.value
        self.horizon_sel.data = self.mapper.horizon.value

    def validate(self):
        if not super().validate():
            return False

        def comm_err(msg):
            self.prompt_sel.errors.append(msg)
            self.sensor_sel.errors.append(msg)

        mapper = Mapper.by_commons(
            prompt=Prompt.by_prime(self.prompt_sel.data),
            sensor=Sensor.by_prime(self.sensor_sel.data),
        )
        if mapper is not None:
            if self.mapper is None:
                comm_err('Combination already present!')
                return False

            if (
                self.mapper.prompt.prime != mapper.prompt.prime
                and self.mapper.sensor.prime != mapper.sensor.prime
            ):
                comm_err('Combination conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.mapper:
            self.mapper = Mapper.create(
                prompt=Prompt.by_prime(self.prompt_sel.data),
                sensor=Sensor.by_prime(self.sensor_sel.data),
                _commit=False,
            )

        self.populate_obj(self.mapper)
        self.mapper.color = EnumColor.from_color(self.color_sel.data)
        self.mapper.convert = EnumConvert(self.convert_sel.data)
        self.mapper.horizon = EnumHorizon(self.horizon_sel.data)
        return self.mapper.save()


class MapperDropForm(GenericDropForm):
    Model = Mapper


class MapperSortForm(GenericSortForm):
    Model = Mapper
