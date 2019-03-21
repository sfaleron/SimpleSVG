
# Will accept iterators or sequences of length two. Always returns Points.

from  __future__ import absolute_import
from  __future__ import division

from collections import namedtuple
from     numbers import Number

# extra symbols for "chained" importing
from        math import sqrt, cos, sin, pi, hypot, atan2

import      attr

# corrections for coordinate system with inverted y-axis
import      math as _math

# negating the dependent vs independent variable amounts to the same thing,
# since sine is an odd function. The inverse tangent is also odd, which
# follows from sine being odd.

## ?? IVY ?? ##
#atan2 = lambda dy,dx: -_math.atan2(dy,dx)


@attr.s(cmp=False)
class IvyTransform(object):
    height = attr.ib()

    def __call__(self, x):
        return self.height-x


class Point(namedtuple('Point', 'x y')):
    def __new__(cls, x, y):
        if isinstance(x, Number):
            if isinstance(y, Number):
                return Point.__bases__[0].__new__(cls, x, y)
            else:
                raise TypeError('y is not a Number')
        else:
            raise TypeError('x is not a Number')

    def __mul__(self, other):
        cls = type(self)

        if isinstance(other, Number):
            return cls(self.x*other, self.y*other)
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        cls = type(self)

        if isinstance(other, Number):
            return cls(self.x/other, self.y/other)
        else:
            return NotImplemented

    __div__ = __truediv__

    def __sub__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            return cls(self.x-other.x, self.y-other.y)
        else:
            return NotImplemented

    def __add__(self, other):
        cls = type(self)

        if isinstance(other, cls):
            return cls(self.x+other.x, self.y+other.y)
        else:
            return NotImplemented

def toPoint(*pts):
    return tuple([pt if isinstance(pt, Point) else Point(*pt) for pt in pts])

def between(pt1, pt2, pos):
    pt1, pt2 = toPoint(pt1, pt2)

    return Point((pt2.x-pt1.x)*pos+pt1.x, (pt2.y-pt1.y)*pos+pt1.y)

def midpoint(pt1, pt2):
    pt1, pt2 = toPoint(pt1, pt2)

    return Point((pt1.x+pt2.x)/2, (pt1.y+pt2.y)/2)

def dist(pt1, pt2):
    pt1, pt2 = toPoint(pt1, pt2)

    return hypot(pt2.x-pt1.x, pt2.y-pt1.y)


def make_scaler(scale):
    class Scale(float):
        def __new__(cls, x):
            return float.__new__(cls, x*scale)

        @property
        def px(self):
            return '{:f}px'.format(self)

    return Scale
