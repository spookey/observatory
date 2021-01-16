from pytest import mark

from observatory.database import Model, SortMixin
from observatory.start.extensions import DB

# pylint: disable=comparison-with-callable
# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class SortMixinPhony(SortMixin, Model):
    num_a = DB.Column(DB.Integer(), nullable=True)
    num_b = DB.Column(DB.Integer(), nullable=True)


@mark.usefixtures('session')
class TestSortMixin:
    @staticmethod
    def test_sortkey():
        srt = SortMixinPhony.create()
        assert srt.sortkey is not None
        assert srt.sortkey == 1

        cls_sortkey = getattr(SortMixinPhony, '_get_class_sortkey', None)
        assert cls_sortkey() == SortMixinPhony.sortkey

    @staticmethod
    def test_sortkey_next():
        for num in range(1, 1 + 23):
            assert SortMixinPhony.sortkey_next() == num
            srt = SortMixinPhony.create(_commit=True)
            assert srt.sortkey == num

    @staticmethod
    def test_sortkey_sticky():
        srt = SortMixinPhony.create()
        assert srt.sortkey == 1

        for field in (SortMixinPhony.prime, SortMixinPhony.sortkey):
            nxt = SortMixinPhony.query.filter(field == 1).first()
            assert nxt is not None
            assert nxt.sortkey == 1

    @staticmethod
    def test_query_sorted():
        one = SortMixinPhony.create(sortkey=1)
        two = SortMixinPhony.create(sortkey=2)
        thr = SortMixinPhony.create(sortkey=3)

        assert SortMixinPhony.query.all() == [one, two, thr]
        assert SortMixinPhony.query_sorted().all() == [thr, two, one]

    @staticmethod
    def test_above_below():
        thr = SortMixinPhony.create(sortkey=3, num_a=1, num_b=1)
        two = SortMixinPhony.create(sortkey=2, num_a=1, num_b=2)
        one = SortMixinPhony.create(sortkey=1, num_a=2, num_b=2)

        assert SortMixinPhony.query.all() == [thr, two, one]
        assert SortMixinPhony.query_sorted().all() == [thr, two, one]

        assert one.query_above().all() == [two, thr]
        assert one.query_below().all() == []
        assert two.query_above().all() == [thr]
        assert two.query_below().all() == [one]
        assert thr.query_above().all() == []
        assert thr.query_below().all() == [one, two]

        qa_one = SortMixinPhony.query.filter(SortMixinPhony.num_a == 1)
        assert one.query_above(query=qa_one).all() == [two, thr]
        assert one.query_below(query=qa_one).all() == []
        assert two.query_above(query=qa_one).all() == [thr]
        assert two.query_below(query=qa_one).all() == []
        assert thr.query_above(query=qa_one).all() == []
        assert thr.query_below(query=qa_one).all() == [two]

        qa_two = SortMixinPhony.query.filter(SortMixinPhony.num_a == 2)
        assert one.query_above(query=qa_two).all() == []
        assert one.query_below(query=qa_two).all() == []
        assert two.query_above(query=qa_two).all() == []
        assert two.query_below(query=qa_two).all() == [one]
        assert thr.query_above(query=qa_two).all() == []
        assert thr.query_below(query=qa_two).all() == [one]

        qb_one = SortMixinPhony.query.filter(SortMixinPhony.num_b == 1)
        assert one.query_above(query=qb_one).all() == [thr]
        assert one.query_below(query=qb_one).all() == []
        assert two.query_above(query=qb_one).all() == [thr]
        assert two.query_below(query=qb_one).all() == []
        assert thr.query_above(query=qb_one).all() == []
        assert thr.query_below(query=qb_one).all() == []

        qb_two = SortMixinPhony.query.filter(SortMixinPhony.num_b == 2)
        assert one.query_above(query=qb_two).all() == [two]
        assert one.query_below(query=qb_two).all() == []
        assert two.query_above(query=qb_two).all() == []
        assert two.query_below(query=qb_two).all() == [one]
        assert thr.query_above(query=qb_two).all() == []
        assert thr.query_below(query=qb_two).all() == [one, two]

    @staticmethod
    def test_raise_lower_step():
        one = SortMixinPhony.create(sortkey=1)
        two = SortMixinPhony.create(sortkey=2)
        thr = SortMixinPhony.create(sortkey=3)
        assert SortMixinPhony.query.all() == [one, two, thr]

        assert SortMixinPhony.query_sorted().all() == [thr, two, one]

        assert one.raise_step() == two
        assert SortMixinPhony.query_sorted().all() == [thr, one, two]

        assert one.raise_step() == thr
        assert SortMixinPhony.query_sorted().all() == [one, thr, two]

        assert one.raise_step() is None
        assert SortMixinPhony.query_sorted().all() == [one, thr, two]

        assert two.raise_step() == thr
        assert SortMixinPhony.query_sorted().all() == [one, two, thr]

        assert SortMixinPhony.query.all() == [one, two, thr]

        assert one.lower_step() == two
        assert SortMixinPhony.query_sorted().all() == [two, one, thr]

        assert one.lower_step() == thr
        assert SortMixinPhony.query_sorted().all() == [two, thr, one]

        assert one.lower_step() is None
        assert SortMixinPhony.query_sorted().all() == [two, thr, one]

        assert thr.raise_step() == two
        assert SortMixinPhony.query_sorted().all() == [thr, two, one]

        assert SortMixinPhony.query.all() == [one, two, thr]

    @staticmethod
    def test_raise_lower_keeps_others():
        one = SortMixinPhony.create(sortkey=1, num_a=1, num_b=2)
        two = SortMixinPhony.create(sortkey=2, num_a=1, num_b=1)
        thr = SortMixinPhony.create(sortkey=3, num_a=2, num_b=1)

        qa_one = SortMixinPhony.query.filter(SortMixinPhony.num_a == 1)
        qa_two = SortMixinPhony.query.filter(SortMixinPhony.num_a == 2)
        qb_one = SortMixinPhony.query.filter(SortMixinPhony.num_b == 1)
        qb_two = SortMixinPhony.query.filter(SortMixinPhony.num_b == 2)

        def _check(flip_a, flip_b):
            assert SortMixinPhony.query_sorted(query=qa_one).all() == (
                [one, two] if flip_a else [two, one]
            )
            assert SortMixinPhony.query_sorted(query=qa_two).all() == [thr]
            assert SortMixinPhony.query_sorted(query=qb_one).all() == (
                [two, thr] if flip_b else [thr, two]
            )
            assert SortMixinPhony.query_sorted(query=qb_two).all() == [one]

        assert SortMixinPhony.query_sorted().all() == [thr, two, one]
        _check(False, False)

        assert one.raise_step() == two
        assert SortMixinPhony.query_sorted().all() == [thr, one, two]
        _check(True, False)

        assert one.raise_step() == thr
        assert SortMixinPhony.query_sorted().all() == [one, thr, two]
        _check(True, False)

        assert two.raise_step() == thr
        assert SortMixinPhony.query_sorted().all() == [one, two, thr]
        _check(True, True)
