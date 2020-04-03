from flask import url_for

from observatory.rest.generic import MapperSlugUrl


def make_obj(**kwargs):
    def obj():
        pass

    for key, val in kwargs.items():
        setattr(obj, key, val)

    return obj


class TestMapperSlugUrl:

    @staticmethod
    def test_empty():
        obj = make_obj()
        res = MapperSlugUrl().patch(obj)

        assert getattr(res, 'prompt_slug', None) is None
        assert getattr(res, 'sensor_slug', None) is None
        assert getattr(res, 'slug', None) is None

    @staticmethod
    def test_unmodified():
        obj = make_obj(
            prompt_slug='unmodified prompt_slug',
            sensor_slug='unmodified sensor_slug',
            slug='unmodified slug',
        )
        res = MapperSlugUrl().patch(obj)

        assert getattr(res, 'prompt_slug', None) == 'unmodified prompt_slug'
        assert getattr(res, 'sensor_slug', None) == 'unmodified sensor_slug'
        assert getattr(res, 'slug', None) == 'unmodified slug'

    @staticmethod
    def test_set_slug():
        obj = make_obj(
            slug='wrong',
            nested=make_obj(slug='real slug'),
        )
        res = MapperSlugUrl(attribute='nested').patch(obj)

        assert getattr(res, 'slug', None) == 'real slug'

    @staticmethod
    def test_set_common_prompt():
        obj = make_obj(
            prompt=make_obj(slug='real prompt_slug'),
            prompt_slug='wrong',
            sensor=make_obj(slug='real sensor_slug'),
            sensor_slug='wrong',
        )

        res = MapperSlugUrl(attribute='prompt').patch(obj)

        assert getattr(res, 'sensor_slug', None) == 'real sensor_slug'
        assert getattr(res, 'prompt_slug', None) == 'real prompt_slug'

    @staticmethod
    def test_output():
        obj = make_obj(slug='test slug')

        for endpoint in ('api.prompt.single', 'api.sensor.single'):
            res = MapperSlugUrl(endpoint=endpoint).output('slug', obj)

            assert res == url_for(endpoint, slug='test slug')
