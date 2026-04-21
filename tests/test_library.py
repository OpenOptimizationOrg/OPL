import pytest
from pydantic import ValidationError

from opltools.schema import (
    Generator,
    Implementation,
    Library,
    Problem,
    Suite,
)


class TestLibrary:
    def test_empty(self):
        lib = Library(root=None)
        assert lib.root is None

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
