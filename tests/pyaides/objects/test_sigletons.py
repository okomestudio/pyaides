from copy import copy
from copy import deepcopy

from pyaides.objects.singletons import MetaSingleton
from pyaides.objects.singletons import Singleton
from pyaides.objects.singletons import singleton


class SubSingleton(Singleton):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Quad:
    def quad(self, x):
        return x ** 2

    def repeat(self, n):
        return self.val * n


class ViaMetaclass(Quad, metaclass=MetaSingleton):
    def __init__(self, *args, val=None, **kwargs):
        self.val = val

    def __str__(self):
        return repr(self) + self.val


class SubViaMetaclass(metaclass=MetaSingleton):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TestViaMetaclass:
    def test_ensure_single_instance(self):
        x = ViaMetaclass(val="sausage")
        assert x.val == "sausage"
        oid = id(x)

        y = ViaMetaclass(val="eggs")
        assert y.val == "eggs"
        assert id(y) == oid
        assert y is x

        z = ViaMetaclass()
        z.val = "spam"
        assert z.val == "spam"
        assert id(z) == oid
        assert z is x

        assert id(x) == oid
        assert id(y) == oid

    def test_copy(self):
        x = ViaMetaclass(val="spam")
        oid = id(x)
        h = copy(x)
        assert id(h) == oid
        assert h is x

    def test_deepcopy(self):
        x = ViaMetaclass(val="spam")
        oid = id(x)
        i = deepcopy(x)
        assert id(i) == oid
        assert i is x

        assert i.quad(2) == 2 ** 2

        assert i.repeat(100) == i.val * 100

    def test_dictval(self):
        x = ViaMetaclass(val={"a": 1, "b": {"c": 2}})
        y = deepcopy(x)
        assert x == y
        y.val["b"]["c"] = 5
        assert x.val["b"]["c"] == y.val["b"]["c"]

    def test_subclassing(self):
        i = ViaMetaclass()
        assert isinstance(i, ViaMetaclass)
        j = SubViaMetaclass(-1, +1)
        assert isinstance(j, SubViaMetaclass)
        assert id(i) != id(j)
        assert ViaMetaclass != SubViaMetaclass
        assert isinstance(ViaMetaclass, MetaSingleton)
        assert isinstance(SubViaMetaclass, MetaSingleton)


class TestSingleton:
    def test_with_singleton_alone(self):
        s = Singleton()
        assert isinstance(Singleton, MetaSingleton)
        assert isinstance(s, Singleton)

    def test_subsingleton(self):
        s1 = Singleton()
        s2 = SubSingleton(-1, +1)
        assert s2.x == -1
        assert s1 != s2
        assert s1 is not s2


class TestSingletonFactory:
    def test(self):
        xobj = singleton("x")
        assert isinstance(xobj, Singleton)

        yobj = singleton("y")
        assert xobj is not yobj

        xobj2 = singleton("x")
        assert xobj2 is xobj
