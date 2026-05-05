import pytest
from pydantic import ValidationError

from opltools.schema import Link, Reference


class TestReference:
    def test_only_author(self):
        ref = Reference(title="A paper")
        assert ref.title == "A paper"
        assert ref.authors is None
        assert ref.link is None

    def test_only_link(self):
        ref = Reference(link=Link(url="https://example.org"))
        assert ref.link.url == "https://example.org"

    def test_full(self):
        ref = Reference(
            title="A paper",
            authors=["Alice"],
            link=Link(url="https://example.org"),
        )
        assert ref.link.url == "https://example.org"

    def test_requires_title_or_link(self):
        with pytest.raises(ValidationError):
            Reference(authors=["A paper"])
