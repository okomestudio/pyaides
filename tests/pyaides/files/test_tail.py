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
    with _fstream("1\n2\n3") as f:
        yield f


@pytest.fixture
def textfile2():
    with _fstream("1\n2\n3\n") as f:
        yield f


class TestTail:
    def test_tail1(self, textfile1):
        n = 2
        assert tail(textfile1, n) == b"3"

    def test_tail2(self, textfile2):
        n = 2
        assert tail(textfile2, n) == b"3"
