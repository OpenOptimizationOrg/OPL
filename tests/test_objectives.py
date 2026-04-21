from opltools.schema import Objectives
from opltools.utils import ValueRange


class TestObjectives:
    def test_default(self):
        obj = Objectives()
        assert obj.root == 0

    def test_int(self):
        assert Objectives(root=3).root == 3

    def test_set(self):
        assert Objectives(root={1, 2, 3}).root == {1, 2, 3}

    def test_range(self):
        obj = Objectives(root=ValueRange(min=1, max=5))
        assert obj.root.min == 1
        assert obj.root.max == 5

    def test_union_ints(self):
        a = Objectives(root=1)
        b = Objectives(root=2)
        a.union(b)
        assert a.root == {1, 2}

    def test_union_same_int(self):
        a = Objectives(root=1)
        b = Objectives(root=1)
        a.union(b)
        assert a.root == 1
