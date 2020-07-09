import pytest

from pyaides.functools import retries


class TestDecorrelatedJitter:
    def test_basic(self):
        state = {"called": 0}

        @retries.decorrelated_jitter(3)
        def g():
            state["called"] += 1
            return state

        assert g()["called"] == 1
        assert g()["called"] == 2

    def test_max_retry_error(self):
        state = {"called": 0}

        @retries.decorrelated_jitter(2, cap=0.5, base=0.1)
        def f():
            state["called"] += 1
            raise ValueError("bomb")

        with pytest.raises(ValueError) as exc:
            f()
        assert str(exc.value) == "bomb"
        assert state["called"] == 2
