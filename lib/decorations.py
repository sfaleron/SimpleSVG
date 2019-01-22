
from __future__ import absolute_import
from __future__ import division

from      .math import Point, dist, between, atan2, pi

import attr

@attr.s(cmp=False)
class Decorations(object):
    tickLength = attr.ib()
    arcRadius  = attr.ib()
    spacing    = attr.ib()

    def arcs(self, ctr, leg0, leg1, bigArc, n, **kw):
        p0 = between(ctr, leg0, self.arcRadius/dist(ctr, leg0))
        p1 = between(ctr, leg1, self.arcRadius/dist(ctr, leg1))

        a0 = atan2(p0.y-ctr.y, p0.x-ctr.x)
        a1 = atan2(p1.y-ctr.y, p1.x-ctr.x)

        if a0>a1:
            p0,p1 = p1,p0
            a0,a1 = a1,a0

            leg0, leg1 = leg1,leg0

        incAngle = bigArc if a1-a0 > pi else not bigArc

        p = Path(p0, **kw)

        r = self.arcRadius

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

        p.close()

        return p

    def ticks(self, p0, p1, n, **kw):
        inc   = self.spacing / dist(p0, p1)
        tick0 = .5 - (n-1)/2*inc

        crossings = [between(p0, p1, tick0+inc*i) for i in range(n)]
        slope     = -(p1.x-p0.x)/(p1.y-p0.y)

        # A slope and a point defines a line; the point is also
        # the center of a circle, the diameter is the tick length.
        # The intersection defines the endpoints of the tick mark.

