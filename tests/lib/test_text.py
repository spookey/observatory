from observatory.lib.text import is_slugable, random_line


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
