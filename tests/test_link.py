import pytest
from pydantic import ValidationError

from opltools.schema import Link


class TestLink:
    def test_minimal(self):
        link = Link(url="https://example.org")
        assert link.url == "https://example.org"
        assert link.type is None

    def test_with_type(self):
        link = Link(type="homepage", url="https://example.org")
        assert link.type == "homepage"

    def test_url_required(self):
        with pytest.raises(ValidationError):
            Link()
