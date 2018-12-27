
# ========================================================
# | Those options you may be looking for are at the end! |
# ========================================================

from __future__ import absolute_import
from __future__ import division

from   .keyattr import KeywordToAttr
from   .math    import Point, pi

class Options(KeywordToAttr):
    __slots__ = ('colors', 'side', 'rotate', 'flip', 'attrs', 'points', 'labels')

    def pick_pts(self, *names):
        return tuple([self.points[k] for k in names])

    @property
    def tri1(self):
        return self.pick_pts('A','B','C')

    @property
    def tri2(self):
        return self.pick_pts('D','E','F')

    @property
    def tri3(self):
        return self.pick_pts('G','H','I')

    @property
    def geo(self):
        xs, ys = zip(*self.tri1)

        xmin   = min(xs); xmax = max(xs)
        ymin   = min(ys); ymax = max(ys)

        return (xmin, ymin, (xmax-xmin), (ymax-ymin))

    @property
    def center(self):
        return Point(*[sum(i)/3 for i in zip(*self.tri1)])

class Colors(KeywordToAttr):
    __slots__ = ('bg', 'slim', 'squat')

class Attributes(KeywordToAttr):
    __slots__ = ('pgon', 'line')

class LabelInfo(KeywordToAttr):
    __slots__ = ('dx', 'dy', 'r', 'theta')


def make_options():
    return Options(side=SIDE, flip=FLIP, rotate=ROTATE,
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

DARK   = '#5c84d0'
DARK   = '#5c84d0'
LIGHT  = '#acc8e4'
BG     = '#e0ecf8'

ROTATE = 0
SIDE   = 200.0
FLIP   = True

pgonAttrs = {'stroke-width' : '0', 'fill-opacity' : '1'}
lineAttrs = {'stroke' : 'black', 'stroke-width' : '{:f}px'.format(3/400*SIDE)}

from .math import outer, inner

A,B,C        = outer( SIDE, ROTATE)
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
