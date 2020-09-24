from flask import url_for
from pytest import mark

from observatory.models.mapper import Mapper

ENDPOINT = 'mgnt.sort_mapper'
VIEW_EP = 'mgnt.view_mapper'


@mark.usefixtures('session')
class TestMgntSortMapper:
    @staticmethod
    @mark.usefixtures('ctx_app')
    @mark.parametrize('direction', ['raise', 'lower'])
    def test_url(direction):
        assert (
            url_for(
                ENDPOINT,
                prompt_slug='test',
                sensor_slug='demo',
                direction=direction,
            )
            == f'/manage/mapper/sort/prompt/test/sensor/demo/{direction}'
        )

    @staticmethod
    def test_no_user(visitor):
        visitor(
            ENDPOINT,
            method='post',
            params={
                'prompt_slug': 'prompt',
                'sensor_slug': 'sensor',
                'direction': 'lower',
            },
            code=401,
        )

    @staticmethod
    def test_form_params(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        url = url_for(
            ENDPOINT,
            prompt_slug=mapper.prompt.slug,
            sensor_slug=mapper.sensor.slug,
            direction='lower',
            _external=True,
        )
        res = visitor(VIEW_EP)
        form = res.soup.select(f'form[action="{url}"]')[-1]
        assert form['method'] == 'POST'

    @staticmethod
    def test_form_fields(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        mapper = Mapper.create(prompt=gen_prompt(), sensor=gen_sensor())
        url = url_for(
            ENDPOINT,
            prompt_slug=mapper.prompt.slug,
            sensor_slug=mapper.sensor.slug,
            direction='lower',
            _external=True,
        )
        res = visitor(VIEW_EP)
        form = res.soup.select(f'form[action="{url}"]')[-1]
        button = form.select('button')[-1]
        assert button.attrs.get('name') == 'submit'
        assert button.attrs.get('type') == 'submit'

    @staticmethod
    def test_form_no_slug(visitor, gen_user_loggedin):
        gen_user_loggedin()
        slug = '🐁'

        res = visitor(
            ENDPOINT,
            method='post',
            params={
                'sensor_slug': slug,
                'prompt_slug': slug,
                'direction': 'raise',
            },
            code=500,
        )

        assert 'no such mapper' in res.soup.text.lower()

    @staticmethod
    def test_form_sorts(visitor, gen_user_loggedin, gen_prompt, gen_sensor):
        gen_user_loggedin()
        one = Mapper.create(
            prompt=gen_prompt('one'), sensor=gen_sensor('one'), sortkey=1
        )
        two = Mapper.create(
            prompt=gen_prompt('two'), sensor=gen_sensor('two'), sortkey=2
        )
        view_url = url_for(VIEW_EP, _external=True)

        def _order(mapper, lift):
            res = visitor(
                ENDPOINT,
                method='post',
                params={
                    'sensor_slug': mapper.sensor.slug,
                    'prompt_slug': mapper.prompt.slug,
                    'direction': 'raise' if lift else 'lower',
                },
                code=302,
            )

            assert res.request.headers['LOCATION'] == view_url
            return Mapper.query_sorted().all()

        assert Mapper.query_sorted().all() == [two, one]

        assert _order(one, True) == [one, two]
        assert _order(one, False) == [two, one]
        assert _order(two, False) == [one, two]
        assert _order(two, True) == [two, one]

        assert _order(two, True) == [two, one]
        assert _order(one, False) == [two, one]
