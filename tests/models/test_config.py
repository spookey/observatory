from datetime import datetime

from pytest import mark, raises
from sqlalchemy.exc import IntegrityError

from stats.models.config import Config
from stats.start.environment import FMT_STRFTIME


@mark.usefixtures('session')
class TestConfig:

    @staticmethod
    def test_default_fields(gen_config):
        start = datetime.utcnow()
        name = 'test'
        title = 'Some test config'
        description = 'Description of some test config'

        config = gen_config(name=name, title=title, description=description)

        assert config.name == name
        assert config.title == title
        assert config.description == description

        assert start <= config.created
        assert config.created <= datetime.utcnow()

        assert config.displays == []

    @staticmethod
    def test_name_unique(gen_config):
        one = gen_config(name='demo', title='one', _commit=False)
        assert one.save(_commit=True)

        two = gen_config(name='demo', title='two', _commit=False)
        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_by_name(gen_config):
        one = gen_config(name='one')
        two = gen_config(name='two')

        assert Config.query.all() == [one, two]

        assert Config.by_name('one') == one
        assert Config.by_name('two') == two

    @staticmethod
    def test_created_fmt(gen_config):
        config = gen_config()
        assert config.created_fmt == config.created.strftime(FMT_STRFTIME)
