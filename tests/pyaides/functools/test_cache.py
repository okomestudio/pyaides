from pathlib import Path
from random import choice
from string import ascii_lowercase
from tempfile import gettempdir
from unittest.mock import Mock

import pytest

from pyaides.functools import cache


@pytest.fixture
def tempdir():
    tdir = Path(gettempdir()) / (
        "pytest-pyaides-" + "".join(choice(ascii_lowercase) for _ in range(8))
    )
    yield tdir
    if tdir.exists():
        for path in tdir.glob("*"):
            path.unlink()
        tdir.rmdir()


class TestCacheToFile:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, monkeypatch, tmpdir):
        monkeypatch.setattr(cache, "DEFAULT_CACHE_DIR", str(tmpdir))
        yield
        tmpdir.remove(rec=1)

    def test_simple(self):
        inner = Mock()

        @cache.cachetofile
        def double(x):
            inner()
            return x * x

        assert double(2) == 4
        inner.assert_called()
        inner.reset_mock()
        assert double(2) == 4
        assert not inner.called

    def test_param_with_none(self):
        inner = Mock()

        @cache.cachetofile()
        def double(x):
            inner()
            return x * x

        assert double(2) == 4
        inner.assert_called()
        inner.reset_mock()
        assert double(2) == 4
        assert not inner.called

    def test_param_with_dir(self, tempdir):
        @cache.cachetofile(tempdir)
        def double(x):
            return x * x

        assert double(2) == 4
        assert tempdir.exists()
        assert sum(1 for _ in tempdir.glob("*"))

    def test_param_with_existing_file(self):
        with pytest.raises(IOError):

            @cache.cachetofile("/dev/null")
            def double(x):
                return x * x
