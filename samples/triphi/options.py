
from __future__ import absolute_import

from   .keyattr import KeywordToAttr


class Options(KeywordToAttr):
    __slots__ = ('slim', 'squat', 'bg', 'side', 'flip', 'attrs', 'points', 'labels')

    def tri(self, k1,k2,k3):
        return tuple([self.points[k] for k in (k1,k2,k3)])

    @property
    def tri1(self):
        return self.tri('A','B','C')

    @property
    def tri2(self):
        return self.tri('D','E','F')

    @property
    def tri3(self):
        return self.tri('G','H','I')

class Attributes(KeywordToAttr):
    __slots__ = ('pgon', 'line')

class LabelInfo(KeywordToAttr):
    __slots__ = ('dx', 'dy', 'r', 'theta')


def make_options():
    return Options(
        bg     = BG,
        slim   = DARK,  side  = SIDE,
        squat  = LIGHT, flip  = FLIP,

        attrs  = Attributes(pgon=pgonAttrs, line=lineAttrs),

        labels = dict([(i, defaultLabel.copy()) for i in (
            'A','B','C', 'D','E','F', 'G','H','I')]),

        points = dict(zip(
            ('A','B','C', 'D','E','F', 'G','H','I'),
            ( A,  B,  C,   D,  E,  F,   G,  H,  I) ) )
    )


# ====================================================
# | You were expections some options? Here they are! |
# ====================================================

pgonAttrs = {'stroke-width' : '0', 'fill-opacity' : '1'}
lineAttrs = {'stroke' : 'black', 'stroke-width' : '3px'}

DARK  = '#5c84d0'
DARK  = '#5c84d0'
LIGHT = '#acc8e4'
BG    = '#e0ecf8'

SIDE  = 400.0
FLIP  = False

from .math import outer, inner

A,B,C        = outer(SIDE)
D,E,F, G,H,I = inner(A,B,C, FLIP)

# If not specified, r is set to None, which indicates rectangular
# interpretation rather than polar.
defaultLabel = LabelInfo(dx=0, dy=-10)

# ===============
# | Options End |
# ===============
opts = make_options()
