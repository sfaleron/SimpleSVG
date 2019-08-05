
from __future__ import absolute_import

from    .util_  import add_attrSerializer, _serializers

import sys

PY2 = sys.version_info[0] == 2

def unexpression_adder(appendable=None):
    if appendable is None:
        appendable = []
    def dec(unexpression):
        appendable.append(unexpression.__name__)
        return unexpression

    return appendable, dec

def pairfmt(pair):
    return '{},{}'.format(*pair)

def pairsfmt(pairs):
    return ' '.join(map(pairfmt, pairs))


add_attrSerializer(
    shortDesc   = 'Booleans Are Not Strings',
    predicate   = lambda k,v: isinstance(v, bool),
    transformer = lambda k,v: int(v),
    priority    = 9999,
    chain       = False,
    longDesc    = """
    Booleans are caught so that they do not convert to "True" and "False".
    So, if you have a subclass of bool that you don't want converted to an
    int, add a serializer with higher priority (lower numerically). Make
    sure other sorts of booleans are passed through, either by chaining,
    or a predicate that can't match anything other than your type.
    """
)

def attrs_to_xml(dctIn):
    dctOut = {}

    for k,v in sorted(dctIn.items()):
        matches = [serializer for serializer in _serializers if serializer.predicate(k,v)]
        matches.sort(key=lambda e: e.priority)

        for serializer in matches:
            v = serializer.transformer(k,v)
            if not serializer.chain:
                break

        dctOut[k] = v

    return ' ' + ' '.join([ '{}="{}"'.format(
        k, v) for k,v in dctOut.items() ]) if dctIn else ''

class SixDict3(dict):
    """Python2 compatible Python3-dict.
    Methods keys(), values(), and items() are set to their view counterparts."""

    __slots__ = ()

    if PY2:
        keys   = dict.viewkeys
        items  = dict.viewitems
        values = dict.viewvalues
