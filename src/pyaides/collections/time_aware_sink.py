from collections import OrderedDict
from itertools import count
from time import time
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional

# TODO: There needs to be two versions, the one with a fixed TTL and the other with
# varying TTL, for which priority queue may be necessary.


class TimeAwareSink:
    """A set with an object expiry time.

    This is a set which holds objects with expiry time.

    Args:
        arg: An iterable from which to initialize a set.
        ttl: The time to live in seconds.
    """

    def __init__(
        self, arg: Optional[Iterable[Any]] = None, ttl: float = 10, eviction_method=None
    ):
        self._dic: Dict[Any, int] = OrderedDict()
        self.ttl = ttl
        self.eviction_method = NotImplemented
        if arg:
            for i in arg:
                self.add(i)

    def __contains__(self, item: Any) -> bool:
        return self.has(item)

    def __len__(self) -> int:
        self.trim()
        return len(self._dic)

    def _set_expire(self, item: Any):
        t = time()
        expire = t + self.ttl
        if t < expire:
            self._dic[item] = expire
        elif item in self._dic:
            del self._dic[item]

    def add(self, item: Any):
        """Add an item to a set."""
        if item in self._dic:
            self._dic.move_to_end(item)
        else:
            self.trim(1)
        self._set_expire(item)

    def has(self, item: Any) -> bool:
        """Test if an item in a set."""
        return item in self._dic

    def remove(self, item: Any):
        """Remove an item from a set."""
        try:
            self._dic.pop(item)
        except KeyError:
            raise KeyError("item not found")

    def touch(self, item: Any):
        """Touch an item in a set.

        Raises:
            KeyError: If an item is not in a set.
        """
        if item not in self._dic:
            raise KeyError("item not found")
        self._dic.move_to_end(item)
        self._set_expire(item)

    def trim(self, n: Optional[int] = None):
        """Trim a set by ejecting expired item(s) from a set.

        Args:
            n: The max number of items to eject.
        """
        rng = range(0, n) if n else count()
        for _ in rng:
            try:
                item = next(iter(self._dic))
            except StopIteration:
                break
            expire = self._dic[item]
            if expire > time():
                break
            del self._dic[item]
