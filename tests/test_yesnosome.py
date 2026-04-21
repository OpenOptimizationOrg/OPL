import pytest

from opltools.schema import YesNoSome


class TestYesNoSome:
    def test_from_string(self):
        assert YesNoSome("yes") == YesNoSome.yes
        assert YesNoSome("no") == YesNoSome.no
        assert YesNoSome("some") == YesNoSome.some
        assert YesNoSome("?") == YesNoSome.unknown

    def test_bad_string(self):
        with pytest.raises(ValueError):
            YesNoSome("foo")
