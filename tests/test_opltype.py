import pytest

from opltools.schema import OPLType


class TestOPLType:
    def test_from_string(self):
        assert OPLType("problem") is OPLType.problem
        assert OPLType("implementation") is OPLType.implementation
        assert OPLType("suite") is OPLType.suite
        assert OPLType("generator") is OPLType.generator

    def test_bad_string(self):
        with pytest.raises(ValueError):
            OPLType("foo")
