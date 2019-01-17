
from __future__ import print_function
from __future__ import absolute_import

from triphi.keyattr import KeywordToAttr, kw2aDec, AttribItem

@kw2aDec
class Outer(KeywordToAttr):
    _attribs = map(AttribItem, ['a', 'b', 'c'])

@kw2aDec
class Inner(KeywordToAttr):
    _attribs = map(AttribItem, ['x', 'y', 'z'])

cont = Outer(a=42, b=dict(c=99,d=dict(ohmy=None)),
    c=Inner(x='x',y='yes', z=dict(myoh=None)))

cont2 = cont.copy(a=24)


print(cont)
print(cont2)

