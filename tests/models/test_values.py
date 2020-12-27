from pytest import mark

from observatory.models.values import EnumBox, Values

BUCKET = {
    EnumBox.STRING: 'AA',
    EnumBox.NUMBER: 1337,
    EnumBox.SWITCH: True,
}


@mark.usefixtures('session')
class TestValues:
    @staticmethod
    def test_default_fields():
        key = 'test'
        idx = 23

        values = Values.create(key=key, idx=idx)

        assert values.key == key
        assert values.idx == idx
        assert values.box == EnumBox.STRING
        for box in EnumBox:
            assert getattr(values, box.value, 'error') is None

    @staticmethod
    def test_by_key():
        nil_key = 'nil'
        one_key, one_idx = 'one', 23
        two_key, two_idx = 'two', 42
        nil = Values.create(key=nil_key)
        one = Values.create(key=one_key, idx=one_idx)
        two = Values.create(key=two_key, idx=two_idx)

        assert Values.by_key(nil_key) == nil
        assert Values.by_key(nil_key, idx=one_idx) is None
        assert Values.by_key(nil_key, idx=two_idx) is None
        assert Values.by_key(one_key) is None
        assert Values.by_key(one_key, idx=one_idx) == one
        assert Values.by_key(one_key, idx=two_idx) is None
        assert Values.by_key(two_key) is None
        assert Values.by_key(two_key, idx=one_idx) is None
        assert Values.by_key(two_key, idx=two_idx) == two

    @staticmethod
    def test_value_get():
        values = Values.create(
            key='values', **{bx.value: BUCKET[bx] for bx in EnumBox}
        )

        for box, expect in BUCKET.items():
            values.update(box=box)
            assert values.value == expect

    @staticmethod
    def test_value_set():
        values = Values.create(key='values')
        for box in EnumBox:
            assert getattr(values, box.value, 'error') is None

        for box, value in BUCKET.items():
            values.value = value
            for bxx in EnumBox:
                assert getattr(values, bxx.value, 'error') == (
                    value if bxx == box else None
                )
