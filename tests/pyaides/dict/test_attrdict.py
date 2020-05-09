from pyaides.dict.attrdict import attrdict


class TestAttrDict:
    raw = {
        "hosts": {"name": "localhost", "cidr": "127.0.0.1/8"},
        "ip address": "127.0.0.1",
    }

    def test_nested_attrs(self):
        d = attrdict(self.raw)
        assert hasattr(d, "hosts")
        assert hasattr(d.hosts, "name")

    def test_attr_with_space(self):
        d = attrdict(self.raw)
        assert "ip address" in d
        assert hasattr(d, "ip address")
