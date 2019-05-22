import logging

from pyaides.logging.lazy_args import LazyArgs


def test(caplog):
    pars = LazyArgs(x=3, y=lambda o: o["x"] ** 2)
    with caplog.at_level("DEBUG"):
        logging.info("(x, y) = (%(x)d, %(y)d)", pars)
    assert "(x, y) = (3, 9)" in caplog.text
