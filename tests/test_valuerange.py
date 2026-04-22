import pytest
from pydantic import ValidationError

from opltools.utils import ValueRange


class TestValueRange:
    def test_valid(self):
        r = ValueRange(min=1, max=10)
        assert r.min == 1
        assert r.max == 10

    def test_min_only(self):
        r = ValueRange(min=1, max=None)
        assert r.min == 1
        assert r.max is None

    def test_max_only(self):
        r = ValueRange(min=None, max=10)
        assert r.min is None
        assert r.max == 10

    def test_both_none_rejected(self):
        with pytest.raises(ValidationError, match="at least a min or max"):
            ValueRange(min=None, max=None)
