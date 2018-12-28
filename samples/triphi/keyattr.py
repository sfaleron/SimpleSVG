
from collections import Mapping

class ImmDict(Mapping):
    def __init__(self, *args, **kw):
        self._store = dict(*args, **kw)

    def __getitem__(self, key):
        return self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)


class KeywordToAttr(object):
    """Attributes unspecified at instantiation are set to None.

    copy() method deep-copies instances of this class or its
    subclasses and all mappings.

    Mappings must be shallow-copyable by passing the instance
    to its type. For instance, d1 = dict(); d2 = dict(d1)."""

    __slots__  = ()
    _defaults  = ImmDict()
    _noDescent = frozenset()

    def __init__(self, **kw):
        for k in self.__slots__:
            if k in kw:
                setattr(self, k, kw[k])
            else:
                if k in self._defaults:
                    setattr(self, k, self._defaults[k])

    def _copy(self, vIn, **kw):
        if isinstance(vIn, KeywordToAttr):
            vOut = vIn.copy(**kw.get(vIn, {}))

        else:
            if isinstance(vIn, Mapping):
                vOut = type(vIn)(vIn)

                for k,v in kw.items():
                    vOut[k] = self._copy(v)

            else:
                vOut = vIn

        return vOut

    def copy(self, **kw):
        dupe = type(self)()
        for k in self.__slots__:
            if hasattr(self, k):
                setattr(dupe, k, getattr(self, k) if k in self._noDescent
                    else self._copy(getattr(self, k), **kw.get(k, {}) ) )

        return dupe
