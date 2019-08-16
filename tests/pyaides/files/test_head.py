from contextlib import contextmanager
from tempfile import TemporaryFile

from pyaides.files.head import head

import pytest


@contextmanager
def _fstream(text):
    with TemporaryFile("w+b") as f:
        f.write(text.encode("utf-8"))
        f.seek(0)
        yield f


@pytest.fixture
def default():
    with _fstream("1\n22\n\n4444\n") as f:
        yield f


class TestTail:
    @pytest.mark.parametrize(
        "n, expected",
        [(1, b"1\n"), (2, b"1\n22\n"), (3, b"1\n22\n\n"), (10, b"1\n22\n\n4444\n")],
    )
    def test_default(self, n, expected, default):
        assert head(default, n) == expected
