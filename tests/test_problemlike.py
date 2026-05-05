import pytest
from pydantic import ValidationError

from opltools.schema import Problem, ProblemLike, YesNoSome


class TestProblemLike:
    def test_shared_fields(self):
        p = Problem(
            name="P1",
            long_name="Problem 1",
            description="desc",
            tags={"convex", "smooth"},
            allows_partial_evaluation=YesNoSome.yes,
            can_evaluate_objectives_independently=YesNoSome.no,
            modality={"unimodal"},
            fidelity_levels={1, 2, 3},
        )
        assert p.long_name == "Problem 1"
        assert p.tags == {"convex", "smooth"}
        assert p.allows_partial_evaluation is YesNoSome.yes
        assert p.fidelity_levels == {1, 2, 3}

    def test_problemlike_not_directly_useful_without_type(self):
        with pytest.raises(ValidationError):
            ProblemLike(name="X")
