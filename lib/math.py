
# ==================================
# | Use of Point type is presumed! |
# ==================================

from  __future__ import absolute_import
from  __future__ import division

from collections import namedtuple
from     numbers import Number

# extra symbols for "chained" importing
from        math import sqrt, atan2, pi


class Point(namedtuple('Point', 'x y')):
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


def between(pt1, pt2, pos):
    return Point((pt2.x-pt1.x)*pos+pt1.x, (pt2.y-pt1.y)*pos+pt1.y)

def midpoint(pt1, pt2):
    return Point((pt1.x+pt2.x)/2, (pt1.y+pt2.y)/2)

def dist(pt1, pt2):
    return sqrt((pt2.x-pt1.x)**2+(pt2.y-pt1.y)**2)


def make_scaler(scale):
    class Scale(float):
        def __new__(cls, x):
            return float.__new__(cls, x*scale)

        @property
        def px(self):
            return '{:f}px'.format(self)

    return Scale
