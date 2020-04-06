from observatory.models.mapper import EnumColor


def test_enumcolor_color():
    assert EnumColor.BLUE.color == '#4271ae'
    assert EnumColor.BROWN.color == '#a3685a'
    assert EnumColor.GRAY.color == '#969896'
    assert EnumColor.GREEN.color == '#718c00'
    assert EnumColor.ORANGE.color == '#f5871f'
    assert EnumColor.PURPLE.color == '#8959a8'
    assert EnumColor.RED.color == '#c82829'
    assert EnumColor.TURQUOISE.color == '#3e999f'
    assert EnumColor.YELLOW.color == '#eab700'


def test_enumcolor_from_color():
    assert EnumColor.from_color('#c82829') == EnumColor.RED
    assert EnumColor.from_color('4271ae') == EnumColor.BLUE

    assert EnumColor.from_color('123456') == EnumColor.GRAY
    assert EnumColor.from_color('0') == EnumColor.GRAY
    assert EnumColor.from_color(23) == EnumColor.GRAY

    assert EnumColor(7441408) == EnumColor.GREEN
    assert EnumColor.from_color(7441408) == EnumColor.GRAY
