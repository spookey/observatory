from pytest import fixture, mark

from observatory.models.value import EnumBox, Value

# pylint: disable=redefined-outer-name


@fixture(scope='function')
def bucket(gen_sensor):
    sensor = gen_sensor()
    base = {
        EnumBox.STRING: 'AA',
        EnumBox.NUMBER: 1337,
        EnumBox.SWITCH: True,
        EnumBox.SENSOR: None,
    }

    def res():
        pass

    res.obj = {**base, EnumBox.SENSOR: sensor}
    res.key = {**base, EnumBox.SENSOR: sensor.prime}

    yield res


@mark.usefixtures('session')
class TestValue:
    @staticmethod
    def test_bucket(bucket):
        assert bucket.obj.keys() == bucket.key.keys()
        for key, val in bucket.obj.items():
            assert bucket.key[key] == (
                val if key != EnumBox.SENSOR else val.prime
            )

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

        assert value.sensor is None

    @staticmethod
    def test_by_key_idx():
        nil_key = 'nil'
        one_key, one_idx = 'one', 23
        two_key, two_idx = 'two', 42
        nil = Value.create(key=nil_key)
        one = Value.create(key=one_key, idx=one_idx)
        two = Value.create(key=two_key, idx=two_idx)

        assert Value.by_key_idx(key=nil_key) == nil
        assert Value.by_key_idx(key=nil_key, idx=one_idx) is None
        assert Value.by_key_idx(key=nil_key, idx=two_idx) is None
        assert Value.by_key_idx(key=one_key) is None
        assert Value.by_key_idx(key=one_key, idx=one_idx) == one
        assert Value.by_key_idx(key=one_key, idx=two_idx) is None
        assert Value.by_key_idx(key=two_key) is None
        assert Value.by_key_idx(key=two_key, idx=one_idx) is None
        assert Value.by_key_idx(key=two_key, idx=two_idx) == two

    @staticmethod
    def test_by_key():
        key = 'value'
        res = []
        for idx in range(42, 23, -1):
            res.append(Value.create(key=key, idx=idx))

        assert Value.by_key(key='some') == []
        assert Value.by_key(key=key) == list(reversed(res))

    @staticmethod
    def test_elem_property(bucket):
        value = Value.create(
            key='value', **{bx.value: bucket.key[bx] for bx in EnumBox}
        )

        for box, expect in bucket.obj.items():
            value.update(box=box)
            assert value.elem == expect

    @staticmethod
    def test_elem_property_set(bucket):
        value = Value.create(key='value')
        for box in EnumBox:
            assert getattr(value, box.value, 'error') is None

        for box, val in bucket.obj.items():
            value.elem = val
            for bxx, exp in bucket.key.items():
                assert getattr(value, bxx.value, 'error') == (
                    exp if box == bxx else None
                )

    @staticmethod
    def test_elem_property_set_null(bucket):
        value = Value.create(
            key='value', **{bx.value: bucket.key[bx] for bx in EnumBox}
        )

        for box, val in bucket.key.items():
            assert getattr(value, box.value, 'error') == val

        value.elem = None

        for box in bucket.key:
            assert getattr(value, box.value, 'error') is None

    @staticmethod
    def test_get(bucket):
        idx = 23
        for key, obj in bucket.obj.items():
            Value.create(key=f'{key}', idx=idx).update(elem=obj)

        for key, obj in bucket.obj.items():
            assert Value.get(key=f'{key}', idx=idx) == obj

    @staticmethod
    def test_get_all():
        key = 'value'
        for idx in range(42, 23, -1):
            Value.create(key=key, idx=idx).update(elem=idx)

        assert Value.get_all(key='some') == []
        assert Value.get_all(key=key) == list(range(1 + 23, 1 + 42))

    @staticmethod
    def test_set_method():
        past = Value.create(key='past', idx=0)

        assert Value.query.all() == [past]
        assert past.elem is None

        past_elem = 'past'
        done_elem = 23

        Value.set(key='past', idx=0, elem=past_elem)
        done = Value.set(key='done', idx=0, elem=done_elem)

        assert Value.query.all() == [past, done]
        assert past.elem == past_elem
        assert done.elem == done_elem

    @staticmethod
    def test_latest(gen_sensor, gen_user):
        value = Value.create(key='value', idx=42)
        sensor, user = gen_sensor(), gen_user()

        assert value.latest is None
        value.update(elem=23)
        assert value.latest is None

        value.update(elem=sensor)
        assert value.latest is None

        one = sensor.append(user=user, value=23)
        assert value.latest is one

        two = sensor.append(user=user, value=42)
        assert value.latest is two

        assert value.sensor.query_points.all() == [two, one]
