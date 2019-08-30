import pytest

from pyaides.dict.hashable_dict import HashableDict


class TestHashableDict:
    def test_init(self):
        hd = HashableDict(a=1)
        assert hd["a"] == 1

    def test_del(self):
        hd = HashableDict(x=1, y=-1)
        del hd["x"]
        assert "x" not in hd

    def test_equal_true(self):
        assert HashableDict(x=1, y=-1) == HashableDict(y=-1, x=1)

    def test_equal_false(self):
        assert HashableDict(x=2, y=-1) != HashableDict(y=-1, x=1)

    def test_get(self):
        hd = HashableDict(x=1)
        assert "x" in hd
        assert hd["x"] == 1

    def test_get_nonexisting(self):
        hd = HashableDict()
        with pytest.raises(KeyError):
            hd["x"]
        assert hd.get("x") is None

    def test_hash(self):
        hd = HashableDict(x=1, y=-1)
        assert hash(hd) == hd.__hash__()

    def test_hash_equality(self):
        assert HashableDict(x=1, y=-1) == HashableDict(y=-1, x=1)

    def test_hash_inequality(self):
        assert HashableDict(x=1, y=-1) != HashableDict(x=1, y=1)

    def test_iter(self):
        hd = HashableDict(x=1, y=-1)
        assert {"x": 1, "y": -1} == {k: v for k, v in hd.items()}

    def test_len(self):
        assert 2 == len(HashableDict(x=1, y=-1))

    def test_set(self):
        hd = HashableDict()
        assert "x" not in hd
        hd["x"] = 1
        assert "x" in hd
        assert hd["x"] == 1
