from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired

from observatory.forms.base import BaseForm
from observatory.forms.extra.validators import SafeSlug
from observatory.forms.generic import GenericDropForm, GenericSortForm
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor

# pylint: disable=arguments-differ
# pylint: disable=no-member


class CommonEditForm(BaseForm):
    Model = None

    slug = StringField(
        'Slug',
        validators=[DataRequired(), SafeSlug()],
        description='Slug of endpoint',
    )
    title = StringField(
        'Title',
        validators=[DataRequired()],
        description='Title',
    )
    description = TextAreaField(
        'Description',
        description='Description',
    )

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.thing = obj

    def validate(self):
        if not super().validate():
            return False

        thing = self.Model.by_slug(self.slug.data)
        if thing is not None:
            if self.thing is None:
                self.slug.errors.append('Already present!')
                return False

            if self.thing.prime != thing.prime:
                self.slug.errors.append('Slug conflict!')
                return False

        return True

    def action(self):
        if not self.validate():
            return None

        if not self.thing:
            self.thing = self.Model.create(slug=self.slug.data, _commit=False)

        self.populate_obj(self.thing)
        return self.thing.save()


class PromptEditForm(CommonEditForm):
    Model = Prompt

    submit = CommonEditForm.gen_submit_button()


class SensorEditForm(CommonEditForm):
    Model = Sensor

    sticky = BooleanField(
        'Sticky',
        default=False,
        description='Set sticky',
    )
    submit = CommonEditForm.gen_submit_button()


class PromptDropForm(GenericDropForm):
    Model = Prompt


class SensorDropForm(GenericDropForm):
    Model = Sensor


class PromptSortForm(GenericSortForm):
    Model = Prompt


class SensorSortForm(GenericSortForm):
    Model = Sensor
