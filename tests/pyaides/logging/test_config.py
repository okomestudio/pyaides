import logging
import logging.handlers
import sys
from unittest.mock import ANY
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from pyaides.logging.config import _add_handler_to_root
from pyaides.logging.config import _set_level
from pyaides.logging.config import basic_config


class TestBasicConfig:
    @pytest.fixture(autouse=True)
    def setup(self):
        root = logging.root
        for h in root.handlers[:]:
            root.removeHandler(h)
            h.close()

        yield

        root = logging.root
        for h in root.handlers[:]:
            root.removeHandler(h)
            h.close()

    def test_force(self):
        basic_config(force=True)
        assert (
            len(logging.root.handlers) == 1
            and type(logging.root.handlers[0]) == logging.StreamHandler
        ), "basic_config creates at least one StreamHandler"

    def test_no_handlers(self):
        basic_config(force=True, handlers=None)
        assert (
            len(logging.root.handlers) == 1
            and type(logging.root.handlers[0]) == logging.StreamHandler
        ), "basic_config creates at least one StreamHandler"

    @pytest.mark.parametrize("filename, filemode", [("foo", None), ("foo", "a+")])
    def test_no_handlers_and_filename(self, filename, filemode):
        basic_config(force=True, handlers=None, filename=filename)
        assert len(logging.root.handlers) == 1
        handler = logging.root.handlers[0]
        assert type(handler) == logging.FileHandler
        assert handler.baseFilename.endswith("/" + filename)
        assert handler.mode == filemode or "a"

    def test_no_handlers_and_stream(self):
        stream = sys.stdout
        basic_config(force=True, handlers=None, stream=stream)
        assert len(logging.root.handlers) == 1
        handler = logging.root.handlers[0]
        assert type(handler) == logging.StreamHandler
        assert handler.stream == stream

    @pytest.mark.parametrize("host, port", [("localhost", None), ("localhost", 9020)])
    def test_no_handlers_and_socket(self, host, port):
        socket = f"{host}:{port}" if host and port else f"{host}"
        basic_config(force=True, handlers=None, socket=socket)
        assert len(logging.root.handlers) == 1
        handler = logging.root.handlers[0]
        assert type(handler) == logging.handlers.SocketHandler
        assert handler.host == host
        assert handler.port == port or logging.handlers.DEFAULT_TCP_LOGGING_PORT

    def test_handlers(self):
        supplied_handler = logging.handlers.SocketHandler(
            "localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT
        )
        basic_config(force=True, handlers=[supplied_handler])
        assert len(logging.root.handlers) == 1
        handler = logging.root.handlers[0]
        assert type(handler) == type(supplied_handler)

    def test_datefmt(self):
        datefmt = "%Y"
        basic_config(force=True, datefmt="%Y")
        handler = logging.root.handlers[0]
        assert handler.formatter.datefmt == datefmt

    @pytest.mark.parametrize("style", ["%", "$", "{"])
    def test_style(self, style):
        assert style in logging._STYLES
        basic_config(force=True, style=style)
        handler = logging.root.handlers[0]
        assert type(handler.formatter._style) == logging._STYLES[style][0]

    def test_style_error(self):
        style = "X"
        assert style not in logging._STYLES
        with pytest.raises(ValueError):
            basic_config(force=True, style=style)

    def test_filter(self):
        filter = "boto,-moto"
        with patch("pyaides.logging.config._add_handler_to_root") as add:
            basic_config(force=True, filter=filter)
            add.assert_called_once_with(ANY, filter)

    def test_format(self):
        format = "%(message)s"
        basic_config(force=True, format=format)
        handler = logging.root.handlers[0]
        assert handler.formatter._fmt == format

    def test_level(self):
        level = "DEBUG"
        with patch("pyaides.logging.config._set_level") as set_level:
            basic_config(force=True, level=level)
            set_level.assert_called_once_with(ANY, level)

    def test_sentry_client(self):
        level = "DEBUG"
        filter = "boto,-moto"

        class SentryHandler(logging.StreamHandler):
            pass

        with patch(
            "pyaides.logging.config.SentryHandler",
            new=Mock(return_value=SentryHandler()),
        ):
            basic_config(
                force=True,
                sentry_client=Mock(),
                sentry_logging_level=level,
                sentry_logging_filter=filter,
            )
            assert len(logging.root.handlers) == 2
            handler = logging.root.handlers[-1]
            assert type(handler) == SentryHandler
            assert handler.level == getattr(logging, level)

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"filename": "foo", "stream": sys.stdout},
            {"handlers": [logging.StreamHandler()], "filename": "foo"},
            {"handlers": [logging.StreamHandler], "stream": sys.stdout},
        ],
    )
    def test_conflicting_args(self, kwargs):
        with pytest.raises(ValueError) as exc:
            basic_config(force=True, **kwargs)
        assert "should not be specified together" in str(exc.value)

    def test_unknown_args(self):
        with pytest.raises(ValueError) as exc:
            basic_config(force=True, badarg=3)
        assert "Unrecognized argument(s)" in str(exc.value)


class TestSetLevel:
    @pytest.mark.parametrize("level", ["DEBUG", logging.CRITICAL])
    def test_valid_level(self, level):
        handler = logging.StreamHandler()
        _set_level(handler, level)
        assert (
            handler.level == level
            if isinstance(level, int)
            else getattr(logging, level)
        )

    @pytest.mark.parametrize("level", [object()])
    def test_invalid_level(self, level):
        handler = logging.StreamHandler()
        with pytest.raises(TypeError) as exc:
            _set_level(handler, level)
        assert "must be an int or str" in str(exc.value)


class TestAddHandlerToRoot:
    @pytest.fixture(autouse=True)
    def setup(self):
        handlers = logging.root.handlers
        yield
        logging.root.handlers = handlers

    def test(self):
        args = "moto,boto"
        handler = logging.StreamHandler()
        _add_handler_to_root(handler, args)
        assert logging.root.handlers[-1] is handler
