from stats.lib.text import is_safename, random_line


def test_is_safename():
    assert is_safename('test') is True
    assert is_safename('TEST') is True
    assert is_safename('abc-def') is True
    assert is_safename('abc_def') is True
    assert is_safename('abc.def') is True

    assert is_safename('') is False
    assert is_safename(None) is False
    assert is_safename('abc def') is False
    assert is_safename('abc/def') is False
    assert is_safename('abc&def') is False
    assert is_safename('abc=def') is False
    assert is_safename('abc+def') is False
    assert is_safename('abc?def') is False
    assert is_safename('abc@def') is False
    assert is_safename('abc#def') is False
    assert is_safename('💣') is False


def test_random_line():
    pool = ['abc', 'def', 'ghi']
    for _ in range(42):
        assert random_line(pool) in pool


def test_random_line_errors():
    assert random_line(None) == ''
    assert random_line([]) == ''

    assert random_line(['']) == ''
    assert random_line([None]) == ''

    assert random_line([None, False, True, 42]) == ''
