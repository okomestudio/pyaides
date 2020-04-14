import logging
from functools import partial

from pyaides.logging.args import Args


def test(caplog):
    def func(a, b=None):
        return a ** 2 + b

    x = 3
    args = Args(x=x, y=partial(func, x, b=5))
    with caplog.at_level("DEBUG"):
        logging.info("(x, y) = (%(x)d, %(y)d)", args)
    assert "(x, y) = (3, 14)" in caplog.text
