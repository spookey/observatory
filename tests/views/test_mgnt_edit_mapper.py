from flask import url_for
from pytest import mark

from stats.models.mapper import EnumCast, EnumColor, EnumHorizon, Mapper

ENDPOINT = 'mgnt.edit_mapper'


@mark.usefixtures('session')
class TestMgntEditMapper:

    @staticmethod
    @mark.usefixtures('ctx_app')
    def test_url():
        assert url_for(ENDPOINT) == '/manage/mapper/edit'
        assert url_for(
            ENDPOINT, prompt_slug='the_prompt', sensor_slug='the_sensor'
        ) == '/manage/mapper/edit/prompt/the_prompt/sensor/the_sensor'
        assert url_for(
            ENDPOINT, prompt_slug='the_prompt'
        ) == '/manage/mapper/edit/prompt/the_prompt'
        assert url_for(
            ENDPOINT, sensor_slug='the_sensor'
        ) == '/manage/mapper/edit/sensor/the_sensor'

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
            (
                inp.attrs.get('name'),
                inp.attrs.get('type', '_sl_'),
                inp.attrs.get('data-colorize', '_cl_')
            )
            for inp in form.select('input,select')
        ]
        assert fields == [
            ('prompt_sel', '_sl_', '_cl_'),
            ('sensor_sel', '_sl_', '_cl_'),
            ('active', 'checkbox', '_cl_'),
            ('cast_sel', '_sl_', '_cl_'),
            ('color_sel', '_sl_', 'option'),
            ('horizon_sel', '_sl_', '_cl_'),
            ('submit', 'submit', '_cl_'),
        ]

    @staticmethod
    def test_form_wrong(visitor, gen_user_loggedin):
        gen_user_loggedin()

        res = visitor(ENDPOINT, method='post', data={
            'prompt_sel': 23, 'sensor_sel': 42,
            'active': True, 'cast_sel': 99, 'color_sel': 99,
            'horizon_sel': 99, 'submit': True,
        })

        form = res.soup.select('form')[-1]
        assert form.select('#prompt_sel option') == []
        assert form.select('#sensor_sel option') == []
        assert form.select('#active')[-1].attrs['value'] == 'True'
        for sel in [
                '#cast_sel option',
                '#color_sel option',
                '#horizon_sel option'
        ]:
            for opt in form.select(sel):
                assert opt.get('selected') is None
        assert Mapper.query.all() == []

    @staticmethod
    def test_form_creates(visitor, gen_prompt, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        prompt = gen_prompt()
        sensor = gen_sensor()
        cast = EnumCast.INTEGER
        color = EnumColor.YELLOW
        horizon = EnumHorizon.NORMAL
        mgnt_url = url_for('mgnt.index', _external=True)

        res = visitor(ENDPOINT, method='post', data={
            'prompt_sel': prompt.prime, 'sensor_sel': sensor.prime,
            'active': True, 'cast_sel': cast.value, 'color_sel': color.value,
            'horizon_sel': horizon.value, 'submit': True,
        }, code=302)

        assert res.request.headers['LOCATION'] == mgnt_url
        mapper = Mapper.query.first()
        assert mapper.prompt == prompt
        assert mapper.sensor == sensor
        assert mapper.active is True
        assert mapper.cast == cast
        assert mapper.color == color
        assert mapper.horizon == horizon

    @staticmethod
    def test_form_changes(visitor, gen_prompt, gen_sensor, gen_user_loggedin):
        gen_user_loggedin()
        prompt = gen_prompt()
        sensor = gen_sensor()
        original = Mapper.create(prompt=prompt, sensor=sensor)

        cast = EnumCast.BOOLEAN
        color = EnumColor.PURPLE
        horizon = EnumHorizon.INVERT

        visitor(ENDPOINT, params={
            'prompt_slug': prompt.slug, 'sensor_slug': sensor.slug,
        }, method='post', data={
            'prompt_sel': prompt.prime, 'sensor_sel': sensor.prime,
            'active': True, 'cast_sel': cast.value, 'color_sel': color.value,
            'horizon_sel': horizon.value, 'submit': True,
        }, code=302)

        changed = Mapper.query.first()
        assert changed == original
        assert changed.prompt == prompt
        assert changed.sensor == sensor
        assert changed.cast == cast
        assert changed.color == color
        assert changed.horizon == horizon
