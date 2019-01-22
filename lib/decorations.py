
from __future__ import absolute_import
from __future__ import division

from      .math import Point, sqrt, dist, between, atan2, pi
from     ..     import Path

import attr


@attr.s(cmp=False)
class ArcDecorations(object):
    radius  = attr.ib()
    spacing = attr.ib()

    def __call__(self, ctr, leg0, leg1, bigArc=False, n=1, **kw):
        p0 = between(ctr, leg0, self.radius/dist(ctr, leg0))
        p1 = between(ctr, leg1, self.radius/dist(ctr, leg1))

        a0 = atan2(p0.y-ctr.y, p0.x-ctr.x)
        a1 = atan2(p1.y-ctr.y, p1.x-ctr.x)

        if a0>a1:
            p0,p1 = p1,p0
            a0,a1 = a1,a0

            leg0, leg1 = leg1,leg0

        incAngle = bigArc if a1-a0 > pi else not bigArc

        p = Path(p0, **kw)

        r = self.radius

        while n:
            p.arcTo(p1-p0, r, r, 0, bigArc, incAngle)

            n -= 1

            if n:
                r += self.spacing
                leg0, leg1 = leg1,leg0

                p0 = between(ctr, leg0, r/dist(ctr, leg0))
                p.moveTo(p0-p1)

                p1 = between(ctr, leg1, r/dist(ctr, leg0))
                incAngle = not incAngle

        return p


@attr.s(cmp=False)
class TickDecorations(object):
    length  = attr.ib()
    spacing = attr.ib()

    def __call__(self, p0, p1, n=1, **kw):
        inc   = self.spacing / dist(p0, p1)
        tick0 = .5 - (n-1)/2*inc

        crossings = [between(p0, p1, tick0+inc*i) for i in range(n)]

        if abs(p1.y-p0.y)<1e-9:
            slope = None
        else:
            slope = -(p1.x-p0.x)/(p1.y-p0.y)

        # A slope and a point define a line; the point is also the
        # center of a circle, the diameter of which is the tick length.
        # The intersection defines the endpoints of the tick mark.

        pi = crossings[0]

        if slope is None:
            z  = self.length/2
            p0 = Point(pi.x, pi.y-z)
            p1 = Point(pi.x, pi.y+z)
        else:
            z  = self.length/2/sqrt(1+slope**2)
            p0 = Point(pi.x-z, pi.y-slope*z)
            p1 = Point(pi.x+z, pi.y+slope*z)

        p  = Path(p0, **kw)

        while crossings:
            p.lineTo(p1-p0)

            crossings.pop(0)

            if crossings:
                pi = crossings[0]

                if slope is None:
                    p0 = Point(pi.x, pi.y-z)
                    p.moveTo(p0-p1)
                    p1 = Point(pi.x, pi.y+z)
                else:
                    p0 = Point(pi.x-z, pi.y-slope*z)
                    p.moveTo(p0-p1)
                    p1 = Point(pi.x+z, pi.y+slope*z)

        return p
