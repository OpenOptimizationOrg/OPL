from opltools.schema import Implementation, Link, OPLType


class TestImplementation:
    def test_defaults(self):
        impl = Implementation(name="impl1", description="An implementation")
        assert impl.type is OPLType.implementation
        assert impl.name == "impl1"
        assert impl.description == "An implementation"
        assert impl.links is None
        assert impl.language is None
        assert impl.requirements is None

    def test_full(self):
        impl = Implementation(
            name="impl1",
            description="desc",
            links=[Link(url="https://example.org")],
            language="python",
            evaluation_time=["fast"],
            requirements=["numpy", "scipy"],
        )
        assert impl.language == "python"
        assert impl.requirements == ["numpy", "scipy"]
        assert len(impl.links) == 1

    def test_requirements_as_string(self):
        impl = Implementation(
            name="impl1", description="d", requirements="numpy"
        )
        assert impl.requirements == "numpy"
