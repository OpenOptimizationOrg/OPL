import pytest
from pydantic import ValidationError

from opltools.schema import Usage


class TestUsage:
    def test_basic(self):
        u = Usage(language="python", code="print('hi')")
        assert u.language == "python"
        assert u.code == "print('hi')"

    def test_requires_fields(self):
        with pytest.raises(ValidationError):
            Usage(language="python")
