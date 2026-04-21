from opltools.schema import Variables
from opltools.utils import ValueRange


class TestVariables:
    def test_defaults(self):
        v = Variables()
        assert v.continuous == 0
        assert v.integer == 0
        assert v.binary == 0
        assert v.categorical == 0

    def test_explicit_values(self):
        v = Variables(continuous=5, integer=2, binary=1, categorical=3)
        assert v.continuous == 5
        assert v.integer == 2

    def test_range_values(self):
        v = Variables(continuous=ValueRange(min=1, max=10))
        assert v.continuous.min == 1
        assert v.continuous.max == 10

    def test_union(self):
        a = Variables(continuous=1, integer=2)
        b = Variables(continuous=3, integer=4)
        a.union(b)
        assert a.continuous == {1, 3}
        assert a.integer == {2, 4}
