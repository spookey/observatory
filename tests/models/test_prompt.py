from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from stats.models.prompt import Prompt
from stats.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestConfig:

    @staticmethod
    def test_default_fields(gen_prompt):
        start = datetime.utcnow()
        slug = 'test'
        title = 'Some test prompt'
        description = 'Description of some test prompt'

        prompt = gen_prompt(slug=slug, title=title, description=description)

        assert prompt.slug == slug
        assert prompt.title == title
        assert prompt.description == description

        assert start <= prompt.created
        assert prompt.created <= datetime.utcnow()

        assert prompt.mapping == []

    @staticmethod
    def test_slug_unique(gen_prompt):
        one = gen_prompt(slug='demo', title='one', _commit=False)
        assert one.save(_commit=True)

        two = gen_prompt(slug='demo', title='two', _commit=False)
        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_by_slug(gen_prompt):
        one = gen_prompt(slug='one')
        two = gen_prompt(slug='two')

        assert Prompt.query.all() == [one, two]

        assert Prompt.by_slug('one') == one
        assert Prompt.by_slug('two') == two

    @staticmethod
    def test_created_fmt(gen_prompt):
        prompt = gen_prompt()
        assert prompt.created_fmt == prompt.created.strftime(FMT_STRFTIME)
