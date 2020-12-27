from observatory.models.values import EnumBox


def test_enumbox_from_type():
    assert EnumBox.from_type(True) == EnumBox.SWITCH
    assert EnumBox.from_type(False) == EnumBox.SWITCH
    assert EnumBox.from_type(0) == EnumBox.NUMBER
    assert EnumBox.from_type(23.42) == EnumBox.NUMBER
    assert EnumBox.from_type('') == EnumBox.STRING
    assert EnumBox.from_type('test') == EnumBox.STRING
    assert EnumBox.from_type(None) == EnumBox.STRING
    assert EnumBox.from_type(Exception) == EnumBox.STRING
