import pytest
from pydantic import ValidationError

from opltools.schema import Link, Reference


class TestReference:
    def test_minimal(self):
        ref = Reference(title="A paper", authors=["Alice", "Bob"])
        assert ref.title == "A paper"
        assert ref.authors == ["Alice", "Bob"]
        assert ref.link is None

    def test_with_link(self):
        ref = Reference(
            title="A paper",
            authors=["Alice"],
            link=Link(url="https://example.org"),
        )
        assert ref.link.url == "https://example.org"

    def test_requires_authors(self):
        with pytest.raises(ValidationError):
            Reference(title="A paper")
