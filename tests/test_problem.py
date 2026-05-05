from opltools.schema import OPLType, Problem
from opltools.utils import ValueRange


class TestProblem:
    def test_defaults(self):
        p = Problem(name="P1")
        assert p.type is OPLType.problem
        assert p.name == "P1"
        assert p.instances is None

    def test_with_tags_and_objectives(self):
        p = Problem(
            name="P1",
            tags={"convex", "smooth"},
            objectives={1, 2},
        )
        assert p.tags == {"convex", "smooth"}
        assert p.objectives == {1, 2}

    def test_instances_list(self):
        p = Problem(name="P1", instances=["i1", "i2"])
        assert p.instances == ["i1", "i2"]

    def test_instances_range(self):
        p = Problem(name="P1", instances=ValueRange(min=1, max=10))
        assert p.instances.min == 1
        assert p.instances.max == 10
