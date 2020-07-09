import random
import time
from functools import wraps
from logging import Logger
from logging import getLogger
from typing import Any
from typing import Callable
from typing import Optional

log = getLogger(__name__)


def decorrelated_jitter(
    max_retry: int = 1,
    cap: float = 60.0,
    base: float = 1.0,
    logger: Optional[Logger] = None,
    log_level: Optional[str] = "WARNING",
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Retry a function up to ``max_retry`` times upon failure.

    In the following example, the decorated function is retried up to three times if an
    exception occurs::

        >>> @decorrelated_jitter(3)
        >>> def func():
        >>>     # operation(s) to be retried after an Exception.

    In between retries, there will be a sleep, determined by decorrelated jitter based
    on ``cap`` and ``base`` values, where the first sleep is ``t = base`` with the
    subsequent sleeps given by ``t = min(cap, random_between(base, t * 3))`` (see
    [#ref_decorrelated_jitter]).

    Args:
        max_retry: The max number the decorated function is
            retried.
        cap: The maximum sleep time in seconds.
        base: The base sleep time in seconds.
        logger: The logger to which logging messages are sent.
        log_level: Logging level. If :obj:`None`, no retry message gets logged.

    Raises:
        The last exception raised by the wrapped function after the final retry.

    Returns:
        Wrapped function.

    .. [#ref_decorrelated_jitter] https://www.awsarchitectureblog.com/2015/03/backoff.html
    """
    log = logger or globals()["log"]
    log_level = log_level.lower() if log_level else None

    def _retry(f, *args, **kwargs):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            dt = base
            error = None
            for trial in range(max_retry):
                try:
                    rv = f(*args, **kwargs)
                except Exception as exc:
                    dt = min(cap, random.uniform(base, dt * 3.0))
                    if log_level is not None:
                        getattr(log, log_level)(
                            "Retry %d/%d of %s after %.3f sec after %r",
                            trial + 1,
                            max_retry,
                            f.__name__,
                            dt,
                            exc,
                        )
                    time.sleep(dt)
                    error = exc
                    continue
                else:
                    return rv
            else:
                raise error

        return _wrapper

    return _retry
