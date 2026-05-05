from opltools.schema import OPLType, Suite


class TestSuite:
    def test_defaults(self):
        s = Suite(name="S1")
        assert s.type is OPLType.suite
        assert s.problems is None

    def test_with_problems(self):
        s = Suite(name="S1", problems={"p1", "p2"})
        assert s.problems == {"p1", "p2"}
