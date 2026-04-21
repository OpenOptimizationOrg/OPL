from opltools.schema import Constraints


class TestConstraints:
    def test_defaults(self):
        c = Constraints()
        assert c.box == 0
        assert c.linear == 0
        assert c.function == 0

    def test_union(self):
        a = Constraints(box=1, linear=2, function=3)
        b = Constraints(box=4, linear=5, function=6)
        a.union(b)
        assert a.box == {1, 4}
        assert a.linear == {2, 5}
        assert a.function == {3, 6}
