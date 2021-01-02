from pytest import fixture, mark

from observatory.models.mapper import Mapper
from observatory.models.prompt import Prompt
from observatory.models.sensor import Sensor


@fixture(scope='function', params=['prompt', 'sensor', 'mapper'])
def _comm(request, gen_prompt, gen_sensor):
    def res():
        pass

    res.gen_genric, res.model = {
        'prompt': (gen_prompt, Prompt),
        'sensor': (gen_sensor, Sensor),
        'mapper': (
            lambda slug='test', **kwargs: Mapper.create(
                prompt=gen_prompt(slug=f'm_{slug}', **kwargs),
                sensor=gen_sensor(slug=f'm_{slug}', **kwargs),
                **kwargs,
            ),
            Mapper,
        ),
    }.get(request.param)

    yield res


@mark.usefixtures('session')
class TestGeneric:
    @staticmethod
    def test_sortkey_and_next(_comm):
        for num in range(1, 1 + 5):
            assert _comm.model.sortkey_next() == num
            thing = _comm.gen_genric(slug=f'slug_{num}')
            assert thing.sortkey == num

    @staticmethod
    def test_query_sorted(_comm):
        one = _comm.gen_genric(slug='one')
        two = _comm.gen_genric(slug='two')
        thr = _comm.gen_genric(slug='thr')

        assert _comm.model.query.all() == [one, two, thr]
        assert _comm.model.query_sorted().all() == [thr, two, one]

    @staticmethod
    def test_raise_lower_step(_comm):
        thr = _comm.gen_genric(slug='thr', sortkey=3)
        two = _comm.gen_genric(slug='two', sortkey=2)
        one = _comm.gen_genric(slug='one', sortkey=1)

        assert _comm.model.query.all() == [thr, two, one]
        assert _comm.model.query_sorted().all() == [thr, two, one]
        #                               # 321
        assert one.raise_step() == two  # 312
        assert thr.lower_step() == one  # 132
        assert two.raise_step() == thr  # 123

        assert _comm.model.query_sorted().all() == [one, two, thr]

        assert one.raise_step() is None
        assert thr.lower_step() is None

    @staticmethod
    def test_sorted_relations(gen_prompt, gen_sensor):
        p_one = gen_prompt('one', sortkey=1)
        p_two = gen_prompt('two', sortkey=2)
        s_one = gen_sensor('one', sortkey=1)
        s_two = gen_sensor('two', sortkey=2)
        m_one = Mapper.create(prompt=p_one, sensor=s_one, sortkey=1)
        m_two = Mapper.create(prompt=p_one, sensor=s_two, sortkey=2)
        m_thr = Mapper.create(prompt=p_two, sensor=s_two, sortkey=3)

        assert Prompt.query.all() == [p_one, p_two]
        assert Prompt.query_sorted().all() == [p_two, p_one]

        assert Sensor.query.all() == [s_one, s_two]
        assert Sensor.query_sorted().all() == [s_two, s_one]

        assert Mapper.query.all() == [m_one, m_two, m_thr]
        assert Mapper.query_sorted().all() == [m_thr, m_two, m_one]

        assert p_one.mapping == [m_two, m_one]
        assert p_two.mapping == [m_thr]
        assert s_one.mapping == [m_one]
        assert s_two.mapping == [m_thr, m_two]
