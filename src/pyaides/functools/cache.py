import hashlib
import pickle
from functools import wraps
from pathlib import Path

DEFAULT_CACHE_DIR = ".cachetofiledir"


def _ensuredir(path):
    if not path.exists():
        path.mkdir()
    elif not path.is_dir():
        raise IOError(f"'{path}' exists and is not a directory")


def cachetofile(dirname=None):
    """Decorator to wrap a function with a memoizing callable that saves result to disk.

    The decorator works with or without parameters.

    Args:
        dirname: The directory path to which results are cached. Defaults to
            :const:`DEFAULT_CACHE_DIR`.

    Returns:
        Callable wrapped with the decorator.
    """

    def wrapper(func):
        @wraps(func)
        def deco(*args, **kwargs):
            m = hashlib.md5()
            m.update(str((args, kwargs)).encode())
            h = m.hexdigest()
            cachefile = path / (func.__module__ + "." + func.__qualname__ + ":" + h)

            if cachefile.exists():
                with open(cachefile, "rb") as f:
                    result = pickle.load(f)
            else:
                result = func(*args, **kwargs)
                with open(cachefile, "wb") as f:
                    pickle.dump(result, f)

            return result

        return deco

    if callable(dirname):
        func = dirname
        dirname = None
    path = Path(dirname or DEFAULT_CACHE_DIR)
    _ensuredir(path)
    return wrapper if "func" not in locals() else wrapper(func)
