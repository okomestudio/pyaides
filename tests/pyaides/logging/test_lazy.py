import logging

from pyaides.logging.lazy import Lazy


def test(caplog):
    pars = Lazy(x=3, y=lambda o: o["x"] ** 2)
    with caplog.at_level("DEBUG"):
        logging.info("(x, y) = (%(x)d, %(y)d)", pars)
    assert "(x, y) = (3, 9)" in caplog.text
