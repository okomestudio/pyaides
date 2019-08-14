from contextlib import contextmanager
from tempfile import TemporaryFile

from pyaides.files.tail import tail

import pytest


@contextmanager
def _fstream(text):
    with TemporaryFile("w+b") as f:
        f.write(text.encode("utf-8"))
        f.seek(0)
        yield f


@pytest.fixture
def textfile1():
    with _fstream("1\n22\n333\n4444") as f:
        yield f


@pytest.fixture
def textfile2():
    with _fstream("1\n22\n333\n4444\n") as f:
        yield f


class TestTail:
    @pytest.mark.parametrize(
        "n, expected", [(1, b"4444"), (2, b"333\n4444"), (3, b"22\n333\n4444")]
    )
    def test_tail1(self, n, expected, textfile1):
        assert tail(textfile1, n) == expected

    @pytest.mark.parametrize(
        "n, expected", [(1, b"4444"), (2, b"333\n4444"), (3, b"22\n333\n4444")]
    )
    def test_tail2(self, n, expected, textfile2):
        assert tail(textfile2, n) == expected
