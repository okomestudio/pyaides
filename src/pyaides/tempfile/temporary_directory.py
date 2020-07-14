from os.path import exists as path_exists
from shutil import rmtree
from tempfile import mkdtemp
from typing import Optional


class TemporaryDirectory:
    """Create a temporary directory using :func:`tempfile.mkdtemp`.

    The resulting object can be used as a context manager. For example:

      >>>    with TemporaryDirectory() as tmpdir:
      >>>        tmpdir.name  # the path pointing to the temporary file
      >>>        ...

    Upon exiting the context, the directory and everything contained in it are removed.

    Args:
        suffix: If specified, the directory name will end with that suffix; otherwise
                there will be no suffix.
        prefix: If specified, the directory name will start with that prefix; otherwise
                there will be no prefix.
        dir: If specified, the directory will be created in that directory; otherwise, a
             default directory (`/tmp`) will be used.

    Returns:
        A :class:`TemporaryDirectory` object.
    """

    def __init__(
        self,
        suffix: Optional[str] = None,
        prefix: Optional[str] = None,
        dir: Optional[str] = None,
    ):
        self.name = mkdtemp(suffix=suffix or "", prefix=prefix or "tmp", dir=dir)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name!r}>"

    def __enter__(self) -> "TemporaryDirectory":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        if path_exists(self.name):
            rmtree(self.name)
