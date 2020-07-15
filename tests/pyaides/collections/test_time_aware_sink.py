from time import sleep

import pytest

from pyaides.collections.time_aware_sink import TimeAwareSink


class TestTimeAwareSink:
    def test_basic(self):
        chars = "abcde"
        sink = TimeAwareSink(chars, ttl=1)
        assert len(sink) == len(chars)

    def test_expire(self):
        chars = "abcde"
        sink = TimeAwareSink(chars, ttl=-1)
        assert len(sink) == 0

    def test_in(self):
        chars = "abcde"
        sink = TimeAwareSink(chars, ttl=1)
        for c in chars:
            assert c in sink

    def test_not_in(self):
        chars = "abcde"
        sink = TimeAwareSink(chars, ttl=-1)
        for c in chars:
            assert c not in sink

    def test_add(self):
        sink = TimeAwareSink(ttl=1)
        sink.add("a")
        assert "a" in sink

    def test_add_keepalive(self):
        sink = TimeAwareSink(ttl=0.05)
        for _ in range(10):
            sink.add("a")
            sleep(0.05)
        assert "a" in sink

    def test_has(self):
        key = "a"
        sink = TimeAwareSink(key, ttl=1)
        assert (key in sink) is sink.has(key)

    def test_has_not(self):
        key = "a"
        sink = TimeAwareSink()
        assert (key not in sink) is not sink.has(key)

    def test_remove(self):
        key = "a"
        sink = TimeAwareSink(key, ttl=1)
        assert key in sink
        sink.remove(key)
        assert key not in sink

    def test_remove_nonexisting(self):
        sink = TimeAwareSink("a", ttl=-1)
        with pytest.raises(KeyError):
            sink.remove("a")

    def test_touch(self):
        sink = TimeAwareSink("a", ttl=0.1)
        sink.touch("a")

    def test_touch_with_missing_key(self):
        sink = TimeAwareSink()
        with pytest.raises(KeyError):
            sink.touch("a")

    def test_trim(self):
        sink = TimeAwareSink("abc", ttl=0.1)
        assert len(sink._dic) == 3
        sleep(0.2)
        sink.trim()
        assert len(sink._dic) == 0
