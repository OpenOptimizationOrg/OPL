from opltools.utils import ValueRange, union_range


class TestUnionRange:
    def test_int_and_same_int(self):
        assert union_range(3, 3) == 3

    def test_int_and_different_int(self):
        assert union_range(1, 2) == {1, 2}

    def test_int_and_set(self):
        assert union_range(1, {2, 3}) == {1, 2, 3}

    def test_set_and_set(self):
        assert union_range({1, 2}, {2, 3}) == {1, 2, 3}

    def test_set_collapses_to_int(self):
        assert union_range({5}, {5}) == 5

    def test_range_and_range(self):
        a = ValueRange(min=1, max=5)
        b = ValueRange(min=3, max=10)
        result = union_range(a, b)
        assert isinstance(result, ValueRange)
        assert result.min == 1
        assert result.max == 10

    def test_range_and_range_with_none_bounds(self):
        a = ValueRange(min=1, max=None)
        b = ValueRange(min=None, max=10)
        result = union_range(a, b)
        assert result.min == 1
        assert result.max == 10

    def test_range_and_set_extends_max(self):
        r = ValueRange(min=1, max=5)
        result = union_range(r, {10})
        assert isinstance(result, ValueRange)
        assert result.min == 1
        assert result.max == 10

    def test_range_and_set_extends_min(self):
        r = ValueRange(min=5, max=10)
        result = union_range(r, {1})
        assert isinstance(result, ValueRange)
        assert result.min == 1
        assert result.max == 10

    def test_set_and_range_swapped(self):
        r = ValueRange(min=5, max=10)
        result = union_range({1}, r)
        assert isinstance(result, ValueRange)
        assert result.min == 1
        assert result.max == 10

    def test_int_and_range(self):
        r = ValueRange(min=5, max=10)
        result = union_range(1, r)
        assert isinstance(result, ValueRange)
        assert result.min == 1
        assert result.max == 10
