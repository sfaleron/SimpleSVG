
from attrdictbase import ImmutableDict as ImmDict, LazyEval

from collections  import Mapping

class KeywordToAttr(object):
    """Attributes unspecified at instantiation are set to None.

    copy() method deep-copies instances of this class or its
    subclasses and all mappings.

    Mappings must be shallow-copyable by passing the instance
    to its type. For instance, d1 = dict(); d2 = dict(d1)."""

    __slots__  = ()
    _noDescent = frozenset()
    _defaults  = ImmDict()

    def __init__(self, byPos=(), **kw):
        items = dict(byPos)
        items.update(kw)

        for k in self.__slots__:
            if k in items:
                setattr(self, k, items[k])
            else:
                if k in self._defaults:
                    v = self._defaults[k]
                    if isinstance(v, LazyEval):
                        v = v()

                    setattr(self, k, v)

    def update(self, byPos=(), **kw):
        items = dict(byPos)
        items.update(kw)

        for k,v in items.items():
            setattr(self, k, v)

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
