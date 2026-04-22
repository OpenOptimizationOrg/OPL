import pytest

from opltools.schema import YesNoSome
from opltools.yesnosome import union


class TestYesNoSome:
    def test_from_string(self):
        assert YesNoSome("yes") == YesNoSome.yes
        assert YesNoSome("no") == YesNoSome.no
        assert YesNoSome("some") == YesNoSome.some
        assert YesNoSome("?") == YesNoSome.unknown

    def test_bad_string(self):
        with pytest.raises(ValueError):
            YesNoSome("foo")


class TestUnion:
    def test_same_single(self):
        assert union(YesNoSome.yes, YesNoSome.yes) == YesNoSome.yes

    def test_different_singles(self):
        assert union(YesNoSome.yes, YesNoSome.no) == {YesNoSome.yes, YesNoSome.no}

    def test_single_and_set(self):
        result = union(YesNoSome.yes, {YesNoSome.no, YesNoSome.some})
        assert result == {YesNoSome.yes, YesNoSome.no, YesNoSome.some}

    def test_set_and_single(self):
        result = union({YesNoSome.some}, YesNoSome.yes)
        assert result == {YesNoSome.yes, YesNoSome.some}

    def test_set_and_set(self):
        result = union({YesNoSome.yes, YesNoSome.no}, {YesNoSome.no, YesNoSome.some})
        assert result == {YesNoSome.yes, YesNoSome.no, YesNoSome.some}

    def test_set_collapses_to_single(self):
        assert union({YesNoSome.yes}, {YesNoSome.yes}) == YesNoSome.yes
