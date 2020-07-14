import os

from pyaides.tempfile import TemporaryDirectory


class TestTemporaryDirectory:
    def test_without(self):
        td = TemporaryDirectory()
        assert isinstance(td.name, str)
        assert os.path.isdir(td.name)
        td.cleanup()
        assert not os.path.exists(td.name)

    def test_with(self):
        with TemporaryDirectory() as td:
            assert isinstance(td.name, str)
            assert os.path.isdir(td.name)
        assert not os.path.exists(td.name)
