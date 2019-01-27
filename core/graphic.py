
from __future__ import absolute_import

from .base import Element, Style, StyledElement, tagAndRegister

from .path import Path
from .util import pairsfmt, unexpression_adder


__all__, adder = unexpression_adder(['Path'])

@adder
@tagAndRegister('polygon')
class Polygon(StyledElement):
    def __init__(self, pts, **attrs):
        StyledElement.__init__(self, points=pairsfmt(pts), **attrs)

@adder
@tagAndRegister('polyline')
class PolyLine(StyledElement):
    def __init__(self, pts, **attrs):
        StyledElement.__init__(self, points=pairsfmt(pts), **attrs)

@adder
def filled_polygon(pts, fillColor, **attrs):
    return Polygon(pts, fill=fillColor, **attrs)


@adder
@tagAndRegister('line')
class Line(StyledElement):
    def __init__(self, pt1, pt2, **attrs):
        StyledElement.__init__(self,
            x1=pt1[0], y1=pt1[1], x2=pt2[0], y2=pt2[1], **attrs)

@adder
@tagAndRegister('rect')
class Rect(StyledElement):
    def __init__(self, pt, w, h, rx='0', ry='0', **attrs):
        StyledElement.__init__(self,
            x=pt[0], y=pt[1], width=w, height=h, rx=rx, ry=ry, **attrs)

@adder
@tagAndRegister('circle')
class Circle(StyledElement):
    def __init__(self, ctr, r, **attrs):
        StyledElement.__init__(self,
            cx=ctr[0], cy=ctr[1], r=r, **attrs)

@adder
@tagAndRegister('ellipse')
class Ellipse(StyledElement):
    def __init__(self, ctr, rx, ry, **attrs):
        StyledElement.__init__(self,
            cx=ctr[0], cy=ctr[1], rx=rx, ry=ry, **attrs)

@adder
@tagAndRegister('text')
class Text(StyledElement):
    def __init__(self, pt, text, **attrs):
        StyledElement.__init__(self, x=pt[0], y=pt[1], **attrs)
        self.add(text)
