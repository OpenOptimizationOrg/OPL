import pytest
from pydantic import ValidationError

from opltools.schema import (
    Generator,
    Implementation,
    Library,
    Problem,
    Reference,
    Suite,
)


class TestLibrary:
    def test_empty(self):
        lib = Library(root={})
        assert lib.root == {}

    def test_single_problem(self):
        lib = Library(root={"p1": Problem(name="P1")})
        assert "p1" in lib.root
        assert isinstance(lib.root["p1"], Problem)

    def test_multiple_things(self):
        lib = Library(root={
            "p1": Problem(name="P1"),
            "p2": Problem(name="P2"),
            "g1": Generator(name="G1"),
            "s1": Suite(name="S1", problems={"p1", "p2"}),
            "impl1": Implementation(name="impl1", description="d"),
        })
        assert len(lib.root) == 5
        assert isinstance(lib.root["p1"], Problem)
        assert isinstance(lib.root["g1"], Generator)
        assert isinstance(lib.root["s1"], Suite)
        assert isinstance(lib.root["impl1"], Implementation)

    def test_suite_references_missing_problem(self):
        with pytest.raises(ValidationError, match="undefined id"):
            Library(root={
                "s1": Suite(name="S1", problems={"does-not-exist"}),
            })

    def test_suite_references_non_problem(self):
        with pytest.raises(ValidationError, match="but id is a"):
            Library(root={
                "g1": Generator(name="G1"),
                "s1": Suite(name="S1", problems={"g1"}),
            })

    def test_suite_with_no_problems_is_valid(self):
        lib = Library(root={"s1": Suite(name="S1")})
        assert lib.root["s1"].problems is None

    def test_fixup_fidelity_populates_from_problems(self):
        lib = Library(root={
            "p1": Problem(name="P1", fidelity_levels={1, 2}),
            "p2": Problem(name="P2", fidelity_levels={2, 3}),
            "s1": Suite(name="S1", problems={"p1", "p2"}),
        })
        assert lib.root["s1"].fidelity_levels == {1, 2, 3}

    def test_fixup_fidelity_extends_existing(self):
        lib = Library(root={
            "p1": Problem(name="P1", fidelity_levels={5}),
            "s1": Suite(name="S1", problems={"p1"}, fidelity_levels={10}),
        })
        assert lib.root["s1"].fidelity_levels == {5, 10}

    def test_fixup_fidelity_with_problems_without_levels(self):
        lib = Library(root={
            "p1": Problem(name="P1"),
            "p2": Problem(name="P2", fidelity_levels={7}),
            "s1": Suite(name="S1", problems={"p1", "p2"}),
        })
        assert lib.root["s1"].fidelity_levels == {7}

    def test_fixup_fidelity_all_problems_without_levels(self):
        lib = Library(root={
            "p1": Problem(name="P1"),
            "s1": Suite(name="S1", problems={"p1"}),
        })
        assert lib.root["s1"].fidelity_levels == set()

    def test_reference_as_top_level_thing(self):
        lib = Library(root={
            "ref1": Reference(title="A paper"),
            "p1": Problem(name="P1", references={"ref1"}),
        })
        assert isinstance(lib.root["ref1"], Reference)
        assert lib.root["p1"].references == {"ref1"}

    def test_problem_references_missing_reference(self):
        with pytest.raises(ValidationError, match="undefined id"):
            Library(root={
                "p1": Problem(name="P1", references={"does-not-exist"}),
            })

    def test_problem_references_non_reference(self):
        with pytest.raises(ValidationError, match="but id is a"):
            Library(root={
                "p1": Problem(name="P1"),
                "p2": Problem(name="P2", references={"p1"}),
            })

    def test_suite_references_a_reference(self):
        lib = Library(root={
            "ref1": Reference(title="A paper"),
            "p1": Problem(name="P1"),
            "s1": Suite(name="S1", problems={"p1"}, references={"ref1"}),
        })
        assert lib.root["s1"].references == {"ref1"}

    def test_fixup_evaluation_time_percolates_from_implementation_to_suite(self):
        lib = Library(root={
            "impl1": Implementation(
                name="impl1", description="d", evaluation_time={"fast"}
            ),
            "impl2": Implementation(
                name="impl2", description="d", evaluation_time={"8 minutes"}
            ),
            "p1": Problem(name="P1", implementations={"impl1"}),
            "p2": Problem(name="P2", implementations={"impl2"}),
            "s1": Suite(name="S1", problems={"p1", "p2"}),
        })
        assert lib.root["p1"].evaluation_time == {"fast"}
        assert lib.root["p2"].evaluation_time == {"8 minutes"}
        assert lib.root["s1"].evaluation_time == {"fast", "8 minutes"}
