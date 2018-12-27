
# ========================================================
# | Those options you may be looking for are at the end! |
# ========================================================

from __future__ import absolute_import

from   .keyattr import KeywordToAttr


class Options(KeywordToAttr):
    __slots__ = ('colors', 'side', 'flip', 'attrs', 'points', 'labels')

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

class Colors(KeywordToAttr):
    __slots__ = ('bg', 'slim', 'squat')

class Attributes(KeywordToAttr):
    __slots__ = ('pgon', 'line')

class LabelInfo(KeywordToAttr):
    __slots__ = ('dx', 'dy', 'r', 'theta')


def make_options():
    return Options(side=SIDE, flip=FLIP,
        colors = Colors(bg=BG, slim=DARK, squat=LIGHT),

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
FLIP  = True

from .math import outer, inner

A,B,C        = outer(SIDE)
D,E,F, G,H,I = inner(A,B,C, FLIP)

# If not specified, r is set to None, which indicates rectangular
# interpretation rather than polar.

# The polar attributes are r,theta, with r relative to the side length,
# theta is in radians.
defaultLabel = LabelInfo(dx=0, dy=-10)

# ===============
# | Options End |
# ===============
defaults = make_options()
