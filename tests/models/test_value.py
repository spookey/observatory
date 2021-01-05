from pytest import mark

from observatory.models.value import EnumBox, Value

BUCKET = {
    EnumBox.STRING: 'AA',
    EnumBox.NUMBER: 1337,
    EnumBox.SWITCH: True,
}


@mark.usefixtures('session')
class TestValue:
    @staticmethod
    def test_default_fields():
        key = 'test'
        idx = 23

        value = Value.create(key=key, idx=idx)

        assert value.key == key
        assert value.idx == idx
        assert value.box == EnumBox.STRING
        for box in EnumBox:
            assert getattr(value, box.value, 'error') is None

    @staticmethod
    def test_by_key_idx():
        nil_key = 'nil'
        one_key, one_idx = 'one', 23
        two_key, two_idx = 'two', 42
        nil = Value.create(key=nil_key)
        one = Value.create(key=one_key, idx=one_idx)
        two = Value.create(key=two_key, idx=two_idx)

        assert Value.by_key_idx(nil_key) == nil
        assert Value.by_key_idx(nil_key, idx=one_idx) is None
        assert Value.by_key_idx(nil_key, idx=two_idx) is None
        assert Value.by_key_idx(one_key) is None
        assert Value.by_key_idx(one_key, idx=one_idx) == one
        assert Value.by_key_idx(one_key, idx=two_idx) is None
        assert Value.by_key_idx(two_key) is None
        assert Value.by_key_idx(two_key, idx=one_idx) is None
        assert Value.by_key_idx(two_key, idx=two_idx) == two

    @staticmethod
    def test_by_key():
        key = 'value'
        res = []
        for idx in range(42, 23, -1):
            res.append(Value.create(key=key, idx=idx))

        assert Value.by_key('some') == []
        assert Value.by_key(key) == list(reversed(res))

    @staticmethod
    def test_value_get():
        value = Value.create(
            key='value', **{bx.value: BUCKET[bx] for bx in EnumBox}
        )

        for box, expect in BUCKET.items():
            value.update(box=box)
            assert value.value == expect

    @staticmethod
    def test_value_set():
        value = Value.create(key='value')
        for box in EnumBox:
            assert getattr(value, box.value, 'error') is None

        for box, val in BUCKET.items():
            value.value = val
            for bxx in EnumBox:
                assert getattr(value, bxx.value, 'error') == (
                    val if bxx == box else None
                )

    @staticmethod
    def test_get():
        one_key, one_idx, one_val = 'one', 23, BUCKET[EnumBox.STRING]
        two_key, two_idx, two_val = 'two', 42, BUCKET[EnumBox.NUMBER]
        thr_key, thr_idx, thr_val = 'thr', 55, BUCKET[EnumBox.SWITCH]
        Value.create(key=one_key, idx=one_idx).update(value=one_val)
        Value.create(key=two_key, idx=two_idx).update(value=two_val)
        Value.create(key=thr_key, idx=thr_idx).update(value=thr_val)

        assert Value.get(one_key, idx=one_idx) == one_val
        assert Value.get(two_key, idx=two_idx) == two_val
        assert Value.get(thr_key, idx=thr_idx) == thr_val

    @staticmethod
    def test_get_all():
        key = 'value'
        for idx in range(42, 23, -1):
            Value.create(key=key, idx=idx).update(value=idx)

        assert Value.get_all('some') == []
        assert Value.get_all(key) == list(range(1 + 23, 1 + 42))

    @staticmethod
    def test_set():
        past = Value.create(key='past', idx=0)

        assert Value.query.all() == [past]
        assert past.value is None

        past_val = 'past'
        done_val = 23

        Value.set(key='past', idx=0, value=past_val)
        done = Value.set(key='done', idx=0, value=done_val)

        assert Value.query.all() == [past, done]
        assert past.value == past_val
        assert done.value == done_val
