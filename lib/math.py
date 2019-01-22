
from  __future__ import absolute_import
from  __future__ import division

from collections import namedtuple
from        math import sqrt, atan2, pi


class Point(namedtuple('Point', 'x y')):
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

def between(p1, p2, pos):
    return Point((p2.x-p1.x)*pos+p1.x, (p2.y-p1.y)*pos+p1.y)

def midpoint(p1, p2):
    return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

def dist(p1, p2):
    return sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
