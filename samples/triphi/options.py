
# ========================================================
# | Those options you may be looking for are at the end! |
# ========================================================

from   __future__ import absolute_import
from   __future__ import division

from     .keyattr import KeywordToAttr, kw2aDec, AttribItem
from     .math    import Point, pi

from filterplexer import FilterPlexer, FilterPlexerMeta

from          six import add_metaclass

@kw2aDec
class Options(KeywordToAttr):
    _attribs = map(AttribItem, [
        'colors', 'side', 'rotate', 'flip', 'attrs', 'points', 'labels'])

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
    def dims(self):
        return self.geo[2:]

    @property
    def center(self):
        return Point(*[sum(i)/3 for i in zip(*self.tri1)])

@kw2aDec
class Colors(KeywordToAttr):
    _attribs = map(AttribItem, ['bg', 'slim', 'squat'])

def make_norm_attrs(parent):
    @add_metaclass(FilterPlexerMeta)
    class WithNormalizedStrokeWidth(dict):
        filters = FilterPlexer()
        @filters.out(['__init__', '__setitem__', 'setdefault', 'update'])
        def normalize(self, result):
            if self.get('stroke-width', '').endswith('nm'):
                self['stroke-width'] = '{:f}px'.format(float(
                    self['stroke-width'][:-2])*parent.side/standardSide)

            return result

    return WithNormalizedStrokeWidth

@kw2aDec
class Attributes(KeywordToAttr):
    _attribs  = (
        AttribItem('pgon', factory=dict),
        AttribItem('line', factory=dict) )

@kw2aDec
class LabelInfo(KeywordToAttr):
    _attribs = (
        AttribItem(    'r'            ),
        AttribItem(   'dx',  default=0),
        AttribItem(   'dy',  default=0),
        AttribItem('theta',  default=0) )


def redraw(options):
    a,b,c = outer(options.side, options.rotate)
    d,e,f, g,h,i = inner(a,b,c, options.flip)

    options.points.update(zip(
            ('A','B','C', 'D','E','F', 'G','H','I'),
            ( a,  b,  c,   d,  e,  f,   g,  h,  i) ) )

def _make_options():
    opts = Options(side=SIDE, flip=FLIP, rotate=ROTATE,
        colors = Colors(bg=BG, slim=DARK, squat=LIGHT),

        labels = dict([(i, defaultLabel.copy()) for i in (
            'A','B','C', 'D','E','F', 'G','H','I')]),

        points = dict(zip(
            ('A','B','C', 'D','E','F', 'G','H','I'),
            ( A,  B,  C,   D,  E,  F,   G,  H,  I) ) )
    )

    NormedAttrs = make_norm_attrs(opts)

    opts.attrs  = Attributes(pgon=NormedAttrs(pgonAttrs), line=NormedAttrs(lineAttrs))

    return opts


standardSide = 480

# ====================================================
# | You were expections some options? Here they are! |
# ====================================================

DARK   = '#5c84d0'
LIGHT  = '#acc8e4'
BG     = '#e0ecf8'

ROTATE = 0
FLIP   = False
SIDE   = standardSide
#SIDE = 200

# "nm" is "normalized", not "nanometers"
#
pgonAttrs = {'stroke-width' : '0', 'fill-opacity' : '1'}
lineAttrs = {'stroke' : 'black', 'stroke-width' : '3nm'}

from .math import outer, inner

A,B,C        = outer( SIDE, ROTATE)
D,E,F, G,H,I = inner(A,B,C, FLIP)

# If not specified, r is set to None, which indicates rectangular
# interpretation rather than polar.

# The polar attributes are r,theta, with r relative to the side length,
# theta is in radians.
defaultLabel = LabelInfo(dx=0, dy=-10)


# modifications when tiling
tileOpts = dict(side=48, rotate=0, flip=FLIP)

# ===============
# | Options End |
# ===============
defaults = _make_options()
