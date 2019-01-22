
# setting attribs the customary way as individual class attributes is
# also supported, and may be combined with attribs declared within the
# _attribs class attribute.

from  collections import Mapping, OrderedDict
from          six import add_metaclass

import       attr


class AttribItem(tuple):
    def __new__(cls, k, **kw):
        return tuple.__new__(cls, [k, kw or dict(default=None)] )


class K2AMeta(type):
    """_attribs may be a mapping or an iterable of key, value pairs"""
    def __new__(mcs, name, bases, dct):
        attribs = dct.pop('_attribs', {})

        if not isinstance(attribs, Mapping):
            attribs = OrderedDict(attribs)

        for k,v in attribs.items():
            dct[k] = attr.ib(**v)

        return type.__new__(mcs, name, bases, dct)


@add_metaclass(K2AMeta)
class KeywordToAttr(object):
    """
    copy() method deep-copies instances of this class or its
    subclasses and all mappings.

    Mappings must be shallow-copyable by passing the instance
    to its type. For instance, d1 = dict(); d2 = dict(d1)."""

    _noDescent = frozenset()

    def __eq__(self, other):
        if isinstance(other, KeywordToAttr):
            return all((getattr(self, name) == getattr(other, name)
                for name in attr.fields(type(self))))
        else:
            return NotImplemented

    def __ne__(self, other):
        x = self==other
        return x if x is NotImplemented else not x

    def update(self, byPos=(), **kw):
        items = dict(byPos)
        items.update(kw)

        for k,v in items.items():
            setattr(self, k, v)


    def _copy(self, vIn, **kw):
        if isinstance(vIn, KeywordToAttr):
            vOut = vIn.copy(**kw)

        else:
            if isinstance(vIn, Mapping):
                vOut = type(vIn)(vIn)

                for k,v in kw.items():
                    vOut[k] = self._copy(v)

            else:
                vOut = vIn

        return vOut


    def copy(self, **kw):
        dupe = attr.evolve(self)
        for k,v in attr.asdict(dupe, recurse=False).items():
            if k in self._noDescent:
                v.update(kw.get(k, {}))
            else:
                setattr(dupe, k, self._copy(v, **kw.get(k, {}) ) )

        return dupe


def kw2aDec(clsIn):
    def initinit(self, byPos=(), **kw):
        items = dict(byPos)
        items.update(kw)

        nextinit(self, **items)

    clsOut   = attr.s(slots=True, cmp=False)(clsIn)
    nextinit = clsOut.__init__

    clsOut.__init__ = initinit

    return clsOut

