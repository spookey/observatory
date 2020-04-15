from datetime import datetime

from pytest import fixture, mark, raises
from sqlalchemy.exc import IntegrityError

from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor
from observatory.start.environment import FMT_STRFTIME


@fixture(scope='function', params=['prompt', 'sensor'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.gen_common, res.model = (
        gen_prompt, Prompt,
    ) if request.param == 'prompt' else (
        gen_sensor, Sensor,
    )

    yield res


@mark.usefixtures('session')
class TestCommon:

    @staticmethod
    def test_default_fields(_comm):
        start = datetime.utcnow()
        slug = 'test'
        title = 'Some test common'
        description = 'Description of some test common'

        thing = _comm.gen_common(
            slug=slug, title=title, description=description
        )

        assert thing.slug == slug
        assert thing.title == title
        assert thing.description == description

        assert thing.sortkey == 1

        assert start <= thing.created
        assert thing.created <= datetime.utcnow()

        assert thing.mapping == []

    @staticmethod
    def test_slug_unique(_comm):
        one = _comm.gen_common(slug='demo', title='one', _commit=False)
        assert one.save(_commit=True)

        two = _comm.gen_common(slug='demo', title='two', _commit=False)
        with raises(IntegrityError):
            assert two.save(_commit=True)

    @staticmethod
    def test_by_slug(_comm):
        one = _comm.gen_common(slug='one')
        two = _comm.gen_common(slug='two')

        assert _comm.model.query.all() == [one, two]

        assert _comm.model.by_slug('one') == one
        assert _comm.model.by_slug('two') == two

    @staticmethod
    def test_created_fmt(_comm):
        thing = _comm.gen_common()
        assert thing.created_fmt == thing.created.strftime(FMT_STRFTIME)

    @staticmethod
    def test_created_epoch(_comm):
        thing = _comm.gen_common()
        assert thing.created_epoch <= (
            thing.created - datetime.utcfromtimestamp(0)
        ).total_seconds()
        assert thing.created_epoch_ms == 1000 * thing.created_epoch
