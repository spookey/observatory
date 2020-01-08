from flask import url_for
from pytest import mark

from stats.models.sensor import Sensor

ENDPOINT = 'mgnt.edit_sensor'


@mark.usefixtures('session')
class TestMgntEditSensor:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/manage/sensor/edit'
        assert url_for(ENDPOINT, name='test') == '/manage/sensor/edit/test'

    @staticmethod
    def test_no_user(visitor):
        visitor(ENDPOINT, code=401)

    @staticmethod
    def test_form_params(visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(ENDPOINT)
        form = res.soup.select('form')[-1]
        assert form['method'] == 'POST'
        assert form['action'] == url_for(ENDPOINT, _external=True)

    @staticmethod
    def test_form_fields(visitor, gen_user_loggedin):
        gen_user_loggedin()
        res = visitor(ENDPOINT)
        form = res.soup.select('form')[-1]

        fields = [
            (inp.attrs.get('name'), inp.attrs.get('type', '_ta_'))
            for inp in form.select('input,textarea')
        ]
        assert fields == [
            ('name', 'text'),
            ('title', 'text'),
            ('description', '_ta_'),
            ('submit', 'submit'),
        ]

    @staticmethod
    def test_form_wrong(visitor, gen_user_loggedin):
        gen_user_loggedin()
        name = '🦏'
        title = ''
        description = 'Wrong!'
        res = visitor(ENDPOINT, method='post', data={
            'name': name, 'title': title,
            'description': description, 'submit': True
        })

        form = res.soup.select('form')[-1]
        assert form.select('#name')[-1].attrs['value'] == name
        assert form.select('#title')[-1].attrs['value'] == title
        assert form.select('#description')[-1].string == description
        assert Sensor.query.all() == []

    @staticmethod
    def test_form_creates(visitor, gen_user_loggedin):
        gen_user_loggedin()
        name = 'my_sensor'
        title = 'My Sensor'
        description = 'This is my Sensor!'
        mgnt_url = url_for('mgnt.index', _external=True)

        res = visitor(ENDPOINT, method='post', data={
            'name': name, 'title': title,
            'description': description, 'submit': True
        }, code=302)

        assert res.request.headers['LOCATION'] == mgnt_url
        sensor = Sensor.query.first()
        assert sensor.name == name
        assert sensor.title == title
        assert sensor.description == description

    @staticmethod
    def test_form_changes(visitor, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        original = gen_sensor()

        name = 'my_sensor'
        title = 'My Sensor'
        description = 'This is my Sensor!'

        visitor(ENDPOINT, params={
            'name': original.name
        }, method='post', data={
            'name': name, 'title': title,
            'description': description, 'submit': True
        }, code=302)

        changed = Sensor.query.first()
        assert changed == original
        assert changed.name == name
        assert changed.title == title
        assert changed.description == description
