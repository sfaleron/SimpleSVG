
from __future__ import print_function

from __future__ import absolute_import
from __future__ import division

from     ..     import Path, Text

from      .math import (
    Point, toPoint, sin, between, pi,
    midpoint, dist, cos, atan2, sqrt )

import re

import attr

@attr.s(cmp=False)
class ArcDecorations(object):
    radius  = attr.ib()
    spacing = attr.ib()

    def __call__(self, ctr, leg0, leg1, bigArc=False, n=1, **kw):
        ctr, leg0, leg1 = toPoint(ctr, leg0, leg1)

        radius  = kw.pop( 'radius',  self.radius)
        spacing = kw.pop('spacing', self.spacing)

        dst0 = dist(ctr, leg0)
        dst1 = dist(ctr, leg1)

        p0 = between(ctr, leg0, radius/dst0)
        p1 = between(ctr, leg1, radius/dst1)

        ## ?? IVY ?? ##
        a0 = atan2(p0.y-ctr.y, p0.x-ctr.x)
        a1 = atan2(p1.y-ctr.y, p1.x-ctr.x)

        if a0>a1:
            p0,p1 = p1,p0
            a0,a1 = a1,a0

            leg0,leg1 = leg1,leg0
            dst0,dst1 = dst1,dst0

        incAngle = bigArc if a1-a0 > pi else not bigArc

        kw['fill-opacity'] = 0
        path = Path(p0, **kw)

        while n:
            path.abs.arcTo(p1, radius, radius, 0, bigArc, incAngle)

            n -= 1

            if n:
                radius += spacing

                leg0, leg1 = leg1,leg0
                dst0, dst1 = dst1,dst0

                p0 = between(ctr, leg0, radius/dst0)
                path.abs.moveTo(p0)

                p1 = between(ctr, leg1, radius/dst1)
                incAngle = not incAngle

        return path


@attr.s(cmp=False)
class CornerDecorations(object):
    """
    Draws straight lines rather than arcs. Intended to implement "right
    angle" figure annotations, but provides functionality analogous to
    the ArcDecorations class.

    "legLength" is defined as the length from the center along each leg
    to the endpoints of the decoration lying on the legs.

    "diagonal" is the distance from the center along the angle bisector
    to the vertex of the corner, somewhat analogous to an arc's radius.
    For a right angle's conventional half-square symbol this is sqrt(2)
    times legLength, which is the default."""

    legLength = attr.ib()
    diagonal  = attr.ib()
    spacing   = attr.ib(default=None)

    @diagonal.default
    def _(self):
        return self.legLength * sqrt(2)

    def __call__(self, ctr, leg0, leg1, bigArc=False, n=1, **kw):
        ctr, leg0, leg1 = toPoint(ctr, leg0, leg1)

        legLength = kw.pop('legLength', self.legLength)
        diagonal  = kw.pop( 'diagonal',  self.diagonal)
        spacing   = kw.pop(  'spacing',   self.spacing)

        diagonalSpacing = diagonal / legLength * spacing

        dst0 = dist(ctr, leg0)
        dst1 = dist(ctr, leg1)

        p0 = between(ctr, leg0, legLength/dst0)
        p1 = between(ctr, leg1, legLength/dst1)

        pm = midpoint( p0, p1)
        dm =     dist(ctr, pm)

        bs0, bs1 = ctr, pm

        if bigArc:
            bs0, bs1 = bs1, bs0

        pv = between(bs0, bs1, diagonal/dm)

        kw['fill-opacity'] = 0
        path = Path(p0, **kw)

        while n:

            path.abs.lineTo(pv)
            path.abs.lineTo(p1)

            n -= 1

            if n:
                legLength += spacing
                diagonal  += diagonalSpacing

                leg0, leg1 = leg1, leg0
                dst0, dst1 = dst1, dst0

                p0 = between(ctr, leg0, legLength/dst0)
                path.abs.moveTo(p0)

                p1 = between(ctr, leg1, legLength/dst1)
                pv = between(bs0,  bs1, diagonal/dm)

        return path


@attr.s(cmp=False)
class HatchDecorations(object):
    length  = attr.ib()
    spacing = attr.ib()

    def __call__(self, pt0, pt1, n=1, **kw):
        pt0, pt1 = toPoint(pt0, pt1)

        length  = kw.pop( 'length',  self.length)
        spacing = kw.pop('spacing', self.spacing)

        inc   = spacing / dist(pt0, pt1)
        tick0 = .5 - (n-1)/2*inc

        crossings = [between(pt0, pt1, tick0+inc*i) for i in range(n)]

        if abs(pt1.y-pt0.y)<1e-9:
            slope = None
        else:
            slope = -(pt1.x-pt0.x)/(pt1.y-pt0.y)

        # A slope and a point define a line; the point is also the
        # center of a circle, the diameter of which is the tick length.
        # The intersection defines the endpoints of the tick mark.

        pti = crossings[0]

        if slope is None:
            z   = length/2
            pt0 = Point(pti.x, pti.y-z)
            pt1 = Point(pti.x, pti.y+z)
        else:
            z   = length/2/sqrt(1+slope**2)
            pt0 = Point(pti.x-z, pti.y-slope*z)
            pt1 = Point(pti.x+z, pti.y+slope*z)

        path = Path(pt0, **kw)

        while crossings:
            path.abs.lineTo(pt1)

            crossings.pop(0)

            if crossings:
                pti = crossings[0]

                if slope is None:
                    pt0 = Point(pti.x, pti.y-z)
                    path.abs.moveTo(pt0)
                    pt1 = Point(pti.x, pti.y+z)
                else:
                    pt0 = Point(pti.x-z, pti.y-slope*z)
                    path.abs.moveTo(pt0)
                    pt1 = Point(pti.x+z, pti.y+slope*z)

        return path


class LineLabel(Text):
    # inverting the order of points is identical to inverting the rotation
    def __init__(self, pt1, pt2, text='', invert=False, **kw):
        pt1, pt2 = toPoint(pt1, pt2)

        if invert:
            pt1,pt2 = pt2,pt1

        midPt = midpoint(pt1, pt2)

        ## ?? IVY ?? ##
        kw.update(transform='rotate({:f} {},{})'.format(
            180/pi * atan2(pt2.y-pt1.y, pt2.x-pt1.x), *midPt))

        kw['text-anchor'] = 'middle'
        Text.__init__(self, midPt, text, **kw)

import sys

def float_out(*args):
    return ','.join(['{:.2f}'.format(arg) for arg in args])

class OhMy(str):
    def __new__(cls, s):
        return str.__new__(cls, s)

def print_(*args):
    for arg in args:
        if isinstance(arg, OhMy):
            print(arg, end='', file=sys.stderr)

        else:
            if not isinstance(arg, Point):
                arg = [arg]

            print(float_out(*arg), file=sys.stderr)


class AngleLabel(Text):
    def __init__(self, ctr, leg0, leg1, radius=None, text='', rotate=0, dx=None, dy=None, **kw):
        ctr, leg0, leg1 = toPoint(ctr, leg0, leg1)

        show = kw.pop('show', False)

        dst0 = dist(ctr, leg0)
        dst1 = dist(ctr, leg1)

        r  = (dst0 + dst1) / 2

        p0 = between(ctr, leg0, r/dst0)
        p1 = between(ctr, leg1, r/dst1)

        ## ?? IVY ?? ##
        a0 = atan2(p0.y-ctr.y, p0.x-ctr.x)
        a1 = atan2(p1.y-ctr.y, p1.x-ctr.x)

        a  = (a0+a1)/2 + rotate

        if show:
            print_(
                ctr,r,OhMy('\n'),
                p0,leg0,dst0,p0.y-ctr.y, p0.x-ctr.x,OhMy('\n'),
                p1,leg1,dst1,p1.y-ctr.y, p1.x-ctr.x,OhMy('\n'),
                a0/pi*180,a1/pi*180,a/pi*180 )

        ## ?? IVY ?? ##
        pt = ctr + Point(
            radius*cos(a) if dx is None else dx,
            radius*sin(a) if dy is None else dy )

        kw['text-anchor'] = 'middle'
        Text.__init__(self, pt, text, **kw)

__all__ = [i+'Decorations' for i in ('Arc', 'Hatch', 'Corner')] + [i+'Label' for i in ('Line', 'Angle')]
