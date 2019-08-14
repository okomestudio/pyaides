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
def end_without_eol():
    with _fstream("1\n22\n333\n4444") as f:
        yield f


@pytest.fixture
def end_with_eol():
    with _fstream("1\n22\n333\n4444\n") as f:
        yield f


@pytest.fixture
def multiple_empty_lines():
    with _fstream("1\n22\n333\n4444\n\n\n") as f:
        yield f


class TestTail:
    @pytest.mark.parametrize(
        "n, expected", [(1, b"4444"), (2, b"333\n4444"), (3, b"22\n333\n4444")]
    )
    def test_tail1(self, n, expected, end_without_eol):
        assert tail(end_without_eol, n) == expected

    @pytest.mark.parametrize(
        "n, expected", [(1, b"4444\n"), (2, b"333\n4444\n"), (3, b"22\n333\n4444\n")]
    )
    def test_tail2(self, n, expected, end_with_eol):
        assert tail(end_with_eol, n) == expected

    @pytest.mark.parametrize(
        "n, expected", [(1, b"\n"), (2, b"\n\n"), (3, b"4444\n\n\n")]
    )
    def test_multiple_empty_lines(self, n, expected, multiple_empty_lines):
        assert tail(multiple_empty_lines, n, 1) == expected
