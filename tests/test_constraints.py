from opltools.schema import Constraint, YesNoSome


class TestConstraint:
    def test_default(self):
        c = Constraint(type="box")
        assert c.hard is None
        assert c.equality is None
        assert c.number is None

    def test_hard(self):
        c = Constraint(type="box", hard="yes")
        assert c.hard == YesNoSome.yes

    def test_number(self):
        c = Constraint(type="linear", number=5)
        assert c.number == 5
