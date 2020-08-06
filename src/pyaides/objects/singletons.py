class MetaSingleton(type):
    instance = {}

    def __init__(cls, name, bases, attrs, **kwargs):
        cls.__copy__ = lambda self: self
        cls.__deepcopy__ = lambda self, memo: self

    def __call__(cls, *args, **kwargs):
        key = cls.__qualname__
        if key not in cls.instance:
            instance = super().__call__(*args, **kwargs)
            cls.instance[key] = instance
        else:
            instance = cls.instance[key]
            instance.__init__(*args, **kwargs)
        return instance


class Singleton(metaclass=MetaSingleton):
    def __init__(self, *args, **kwargs):
        pass


def singleton(name):
    cls = type(name, (Singleton,), {})
    return cls()
