
from collections import Mapping

class KeywordToAttr(object):
    """Attributes unspecified at instantiation are set to None.

    copy() method deep-copies instances of this class or its
    subclasses and all mappings.

    Mappings must be shallow-copyable by passing the instance
    to its type. For instance, d1 = dict(); d2 = dict(d1)."""

    __slots__ = ()

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k, None))

    def _copy(self, vIn, **kw):
        if isinstance(vIn, KeywordToAttr):
            vOut = vIn.copy(**kw.get(k, {}))

        else:
            if isinstance(vIn, Mapping):
                vOut = type(vIn)(vIn)

                for k,v in tuple(kw.items()):
                    vOut[k] = self._copy(v)

            else:
                vOut = vIn

        return vOut

    def copy(self, **kw):
        dupe = type(self)()
        for k in self.__slots__:
            setattr(dupe, k, self._copy(getattr(self, k), **kw.get(k, {}) ))

        return dupe
