from stats.lib.text import is_safename


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
