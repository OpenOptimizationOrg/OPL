from opltools.schema import Constraints, OPLType, Problem, Variables
from opltools.utils import ValueRange


class TestProblem:
    def test_defaults(self):
        p = Problem(name="P1")
        assert p.type is OPLType.problem
        assert p.name == "P1"
        assert p.instances is None

    def test_with_variables_and_constraints(self):
        p = Problem(
            name="P1",
            variables=Variables(continuous=3),
            constraints=Constraints(linear=2),
        )
        assert p.variables.continuous == 3
        assert p.constraints.linear == 2

    def test_instances_list(self):
        p = Problem(name="P1", instances=["i1", "i2"])
        assert p.instances == ["i1", "i2"]

    def test_instances_range(self):
        p = Problem(name="P1", instances=ValueRange(min=1, max=10))
        assert p.instances.min == 1
        assert p.instances.max == 10
