from collections import UserDict


class AttrDict(UserDict):
    pass


def attrdict(d: dict) -> AttrDict:
    """Add attribute access to a dict.

    This function takes a dict with nested dicts as input and convert into an AttrDict
    object which allows attribute access to keys.

    Returns:
        A dict-like object with attribute access to keys.
    """

    def addattrs(d):
        if not isinstance(d, dict):
            return d
        obj = AttrDict()
        for k in d:
            obj[k] = obj.__dict__[k] = addattrs(d[k])
        return obj

    obj = AttrDict()
    obj.update(d)
    obj.__dict__.update(addattrs(d))
    return obj
