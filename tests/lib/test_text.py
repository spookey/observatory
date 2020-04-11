from observatory.lib.text import extract_slug, is_slugable, random_line


def test_random_line():
    pool = ['abc', 'def', 'ghi']
    for _ in range(42):
        assert random_line(pool) in pool


def test_random_line_fallback():
    assert random_line(None) == ''
    assert random_line(None, 'test') == 'test'
    assert random_line(None, None) is None

    assert random_line([]) == ''
    assert random_line([], fallback='demo') == 'demo'

    assert random_line(['']) == ''
    assert random_line([None]) == ''

    assert random_line([None, False, True, 42]) == ''


def test_is_slugable():
    assert is_slugable('test') is True
    assert is_slugable('DEMO') is True
    assert is_slugable('abc-def') is True
    assert is_slugable('abc_def') is True
    assert is_slugable('abc.def') is True

    assert is_slugable('') is False
    assert is_slugable(None) is False
    assert is_slugable('abc def') is False
    assert is_slugable('abc/def') is False
    assert is_slugable('abc&def') is False
    assert is_slugable('abc=def') is False
    assert is_slugable('abc+def') is False
    assert is_slugable('abc?def') is False
    assert is_slugable('abc@def') is False
    assert is_slugable('abc#def') is False
    assert is_slugable('💣') is False


class TestExtractSlug:

    @staticmethod
    def __call__(slug=None, p_slug=None, s_slug=None):
        def res():
            pass

        def prompt():
            pass

        def sensor():
            pass

        if slug is not None:
            setattr(res, 'slug', slug)

        if p_slug is not None:
            res.prompt = prompt
            setattr(res.prompt, 'slug', p_slug)

        if s_slug is not None:
            res.sensor = sensor
            setattr(res.sensor, 'slug', s_slug)

        return res

    def test_common(self):
        assert extract_slug(self(slug='slug')) == 'slug'
        assert extract_slug(self(slug='    ')) == ''

    def test_mapper(self):
        assert extract_slug(
            self(p_slug='prompt', s_slug='sensor')
        ) == 'prompt sensor'
        assert extract_slug(
            self(p_slug='      ', s_slug='sensor')
        ) == 'sensor'
        assert extract_slug(
            self(p_slug='prompt', s_slug='      ')
        ) == 'prompt'
        assert extract_slug(
            self(p_slug='      ', s_slug='      ')
        ) == ''

    def test_both(self):
        assert extract_slug(
            self(slug='slug', p_slug='prompt', s_slug='sensor')
        ) == 'slug'
        assert extract_slug(
            self(slug='slug', p_slug='      ', s_slug='sensor')
        ) == 'slug'
        assert extract_slug(
            self(slug='slug', p_slug='prompt', s_slug='      ')
        ) == 'slug'
        assert extract_slug(
            self(slug='    ', p_slug='prompt', s_slug='sensor')
        ) == ''
