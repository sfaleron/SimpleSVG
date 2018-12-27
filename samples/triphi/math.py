
from __future__ import print_function

from __future__ import absolute_import
from __future__ import division

from math import sin, cos, pi, atan2

from collections import namedtuple


Point = namedtuple('Point', ('x', 'y'))

def between(p1, p2, pos):
    return Point((p1.x-p2.x)*pos+p2.x, (p1.y-p2.y)*pos+p2.y)

def midpoint(p1, p2):
    return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)


# Construct a figure like that at http://www.cut-the-knot.org/do_you_know/Buratino7.shtml
# our points are labeled counterclockwise, which doesn't always correspond to the diagram on this page
#
# Maybe later: http://www.cut-the-knot.org/do_you_know/Buratino2.shtml
#
# Not triangular, but also interesting: http://www.cut-the-knot.org/do_you_know/Buratino6.shtml


####################################
# first, find the outermost triangle
#
# the Law of Cosines says
# a^2 + b^2 - 2*a*b*cos(C) = c^2
#
# c is the subtended chord, and one side of the triangle
# a and b are radii, and C is 120 degrees. easy-peasy!
#
# 2*r^2 + r^2 = s^2
# sqrt(3)*r = s
#
def outer(sideLength, rotate=0):
    """sideLength is in pixels, rotate in radians"""

    # side*1/sqrt(3), or half of the height of the triangle
    r = sideLength*3**-2**-1

    pts = [ Point(r*cos(a), r*sin(a)) for a in [
        (2./3*i+.5)*pi+rotate for i in range(3)] ]

    xs, ys = zip(*pts)

    xmin = min(xs); xmax = max(xs)
    ymin = min(ys); ymax = max(ys)

    # for an SVG canvas (inverted y)
    transform = lambda p: Point(p.x-xmin, ymax-p.y)

    return tuple(map(transform, pts))


####################################################
# Find the inner triangle with vertices on the sides
# of the first triangle, and the innermost triangle,
# who's vertices are the midpoints of the first.
#
# D is colinear with AB, and the length of BD is the
# outermost side length AB divided by phi.
#
# Yeah, it'd be nice to have phi fall out of some equations, rather
# than using it explicitly, but there's a geometric proof on the web
# page cited, and crunching it algebraicly would only result in ex-
# pressions equivalent to what is here. I haven't done it yet, but I
# would start by paramaterizing the inner triangle by the position of
# one vertex along a side of the outer triangle and setting the mid-
# points of the inner triangle to be colinear with the appropriate
# vertex of the outer triangle.

def inner(A, B, C, flip=False):

    invphi = 2/(1+5**2**-1)

    if flip:
        invphi = 1-invphi

    D = between(B, C, invphi)
    E = between(C, A, invphi)
    F = between(A, B, invphi)

    G = midpoint(D, E)
    H = midpoint(E, F)
    I = midpoint(F, D)

    return (D,E,F, G,H,I)


# Given two points defining a side, find the remaining vertices of
# the two equilateral triangles that share this side.
#
# Draw a line perpendicular to the side, at its midpoint, and go along
# the line for sqrt(3)/2 times the side length units.
#
# y-y1=m*(x-x1)
# m = -1/((y2-y1)/(x2-x1))
#
# y = (x1-x2)(x-x3)/(y2-y1)+y3 (1)
#
# Equation of the circle centered on the midpoint with the radius desired
# 3/4*s^2 = (y-y3)^2+(x-x3)^2  (2)
#
# Substitute (1) for y, solve for x
#
# x = x3 +/- sqrt(3/4)*s*
#     (y2-y1)/sqrt(x1^2+x2^2+y1^2+y2^2 - 2*(x1*x2+y1*y2))
#
# Substitute into (1) and solve for y
#
# y = y3 -/+ sqrt(3/4)*s*
#     (x2-x1)/sqrt(x1^2+x2^2+y1^2+y2^2 - 2*(x1*x2+y1*y2))
#
# It's worth pointing out there's no possible zeros in denominators here!
#
# At least if p1 and p2 are not the same point. Horizontal and vertical
# sides work fine. This is the only condition (among real numbers) for
# x1^2+x2^2+y1^2+y2^2 = 2*(x1*x2+y1*y2), according to Wolfram Alpha.
#
def triangles_from_side(p1, p2, sideLength=None):
    """Given two points defining a side, find the remaining vertices of
    the two equilateral triangles that share this side. A bit of
    calculating can be averted if the side length is handy when calling,
    or the third argument can be used to find isoceles triangles rather
    than equilateral. The height of the triangles is sqrt(3)/2*sideLength.

    Returns two A,B,C triples, in counterclockwise order, in the same
    manner as two calls to outer()."""

    midPt   = midpoint(p1, p2)

    if sideLength is None:
        # sideLength is a sqrt, makes sense to combine radicals
        a,b = 1, (p1.x-p2.x)**2 + (p1.y-p2.y)**2
    else:
        a,b = sideLength, 1

    k = a/2 * (3*b / (
        p1.x**2 + p2.x**2 + p1.y**2 + p2.y**2 - 2*(p1.x*p2.x + p1.y*p2.y)))**.5

    p3a = Point(midPt.x - (p2.y-p1.y)*k, midPt.y + (p2.x-p1.x)*k)
    p3b = Point(midPt.x + (p2.y-p1.y)*k, midPt.y - (p2.x-p1.x)*k)

    return (make_ccw([p1,p2,p3a], midPt), make_ccw([p1,p2,p3b], midPt))



# flip the y for SVG
def make_ccw(pts, ctr):
    return tuple(zip(*sorted(
        [(pt, atan2(ctr.y-pt.y, pt.x-ctr.x)) for pt in pts], key=lambda x:x[1]) ))[0]


def mkdumpfunc(lw, rw):
    fmtstr = ' '.join([','.join(['%%%d.%df' % (lw+rw+1, rw)]*2)]*3)
    return lambda p1, p2, p3: fmtstr % (p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)

if __name__ == '__main__':

    A,B,C        = outer(400)
    D,E,F, G,H,I = inner(A,B,C)

    dumpfunc     = mkdumpfunc(3, 4)

    print(dumpfunc(A, B, C))
    print(dumpfunc(D, E, F))
    print(dumpfunc(G, H, I))