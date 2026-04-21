from opltools.schema import Variable, VariableType
from opltools.utils import ValueRange


class TestVariable:
    def test_defaults(self):
        v = Variable()
        assert v.type is VariableType.unknown
        assert v.dim == 0

    def test_explicit_values(self):
        v = Variable(type="continuous", dim=5)
        assert v.type is VariableType.continuous
        assert v.dim == 5

    def test_range_dim(self):
        v = Variable(type="integer", dim=ValueRange(min=1, max=10))
        assert v.dim.min == 1
        assert v.dim.max == 10

    def test_set_dim(self):
        v = Variable(type="binary", dim={2, 4})
        assert v.dim == {2, 4}
