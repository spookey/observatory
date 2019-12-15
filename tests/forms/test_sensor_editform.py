from pytest import mark
from werkzeug.datastructures import MultiDict

from stats.forms.sensor import SensorEditForm
from stats.models.sensor import Sensor


@mark.usefixtures('session', 'ctx_app')
class TestSensorEditForm:

    @staticmethod
    def test_basic_fields():
        form = SensorEditForm()
        assert form.name is not None
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
    def test_no_safe_name():
        form = SensorEditForm(name='🐭', title='t')
        assert form.validate() is False
        assert 'safe name' in form.name.errors[-1].lower()

    @staticmethod
    def test_already_present(gen_sensor):
        sensor = gen_sensor()
        form = SensorEditForm(name=sensor.name, title='t')
        assert form.validate() is False
        assert 'already present' in form.name.errors[-1].lower()

    @staticmethod
    def test_name_conflict(gen_sensor):
        orig = gen_sensor(name='original')
        edit = gen_sensor(name='editing')
        form = SensorEditForm(
            obj=edit, formdata=MultiDict({'name': orig.name})
        )
        assert form.validate() is False
        assert 'name conflict' in form.name.errors[-1].lower()

    @staticmethod
    def test_edit_exisiting(gen_sensor):
        name = 'changed_sensor'
        title = 'The changed sensor'
        description = 'Some changed sensor for testing'

        sensor = gen_sensor()
        assert Sensor.query.all() == [sensor]
        form = SensorEditForm(
            obj=sensor, formdata=MultiDict({
                'name': name, 'title': title, 'description': description,
            })
        )
        assert form.validate() is True
        edited = form.action()
        assert edited.name == name
        assert edited.title == title
        assert edited.description == description
        assert edited == sensor
        assert Sensor.query.all() == [edited]

    @staticmethod
    def test_create_new():
        name = 'sensor'
        title = 'The Sensor'
        description = 'Some Sensor for testing'

        form = SensorEditForm(name=name, title=title, description=description)
        assert form.validate() is True
        sensor = form.action()
        assert sensor.name == name
        assert sensor.title == title
        assert sensor.description == description

        assert Sensor.query.all() == [sensor]
