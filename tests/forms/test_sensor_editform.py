from pytest import mark
from werkzeug.datastructures import MultiDict

from stats.forms.sensor import SensorEditForm
from stats.models.sensor import Sensor


@mark.usefixtures('session', 'ctx_app')
class TestSensorEditForm:

    @staticmethod
    def test_basic_fields():
        form = SensorEditForm()
        assert form.slug is not None
        assert form.title is not None
        assert form.description is not None
        assert form.submit is not None

    @staticmethod
    def test_empty_sensor():
        form = SensorEditForm()
        assert form.sensor is None

    @staticmethod
    def test_obj_sensor():
        obj = '🦉'
        form = SensorEditForm(obj=obj)
        assert form.sensor == obj

    @staticmethod
    def test_empty_invalid():
        form = SensorEditForm()
        assert form.validate() is False
        assert form.action() is None
        assert form.sensor is None

    @staticmethod
    def test_no_safe_slug():
        form = SensorEditForm(slug='🐭', title='t')
        assert form.validate() is False
        assert 'safe slug' in form.slug.errors[-1].lower()

    @staticmethod
    def test_already_present(gen_sensor):
        sensor = gen_sensor()
        form = SensorEditForm(slug=sensor.slug, title='t')
        assert form.validate() is False
        assert 'already present' in form.slug.errors[-1].lower()

    @staticmethod
    def test_slug_conflict(gen_sensor):
        orig = gen_sensor(slug='original')
        edit = gen_sensor(slug='editing')
        form = SensorEditForm(
            obj=edit, formdata=MultiDict({'slug': orig.slug})
        )
        assert form.validate() is False
        assert 'slug conflict' in form.slug.errors[-1].lower()

    @staticmethod
    def test_edit_exisiting(gen_sensor):
        slug = 'changed_sensor'
        title = 'The changed sensor'
        description = 'Some changed sensor for testing'

        sensor = gen_sensor()
        assert Sensor.query.all() == [sensor]
        form = SensorEditForm(
            obj=sensor, formdata=MultiDict({
                'slug': slug, 'title': title, 'description': description,
            })
        )
        assert form.validate() is True
        edited = form.action()
        assert edited.slug == slug
        assert edited.title == title
        assert edited.description == description
        assert edited == sensor
        assert Sensor.query.all() == [edited]

    @staticmethod
    def test_create_new():
        slug = 'sensor'
        title = 'The Sensor'
        description = 'Some Sensor for testing'

        form = SensorEditForm(slug=slug, title=title, description=description)
        assert form.validate() is True
        sensor = form.action()
        assert sensor.slug == slug
        assert sensor.title == title
        assert sensor.description == description

        assert Sensor.query.all() == [sensor]
