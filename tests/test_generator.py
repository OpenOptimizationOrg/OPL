from opltools.schema import Generator, OPLType


class TestGenerator:
    def test_defaults(self):
        g = Generator(name="G1")
        assert g.type is OPLType.generator
