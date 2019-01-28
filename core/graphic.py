
from __future__ import absolute_import

from .base import Element, Style, register

from .path import Path
from .util import pairsfmt, unexpression_adder


__all__, adder = unexpression_adder(['Path'])

@adder
@register('polygon', 'styled')
class Polygon(Element):
    def __init__(self, pts, **attrs):
        Element.__init__(self, points=pairsfmt(pts), **attrs)

@adder
@register('polyline', 'styled')
class PolyLine(Element):
    def __init__(self, pts, **attrs):
        Element.__init__(self, points=pairsfmt(pts), **attrs)

@adder
def filled_polygon(pts, fillColor, **attrs):
    return Polygon(pts, fill=fillColor, **attrs)


@adder
@register('line', 'styled')
class Line(Element):
    def __init__(self, pt1, pt2, **attrs):
        Element.__init__(self,
            x1=pt1[0], y1=pt1[1], x2=pt2[0], y2=pt2[1], **attrs)

@adder
@register('rect', 'styled')
class Rect(Element):
    def __init__(self, pt, w, h, rx='0', ry='0', **attrs):
        Element.__init__(self,
            x=pt[0], y=pt[1], width=w, height=h, rx=rx, ry=ry, **attrs)

@adder
@register('circle', 'styled')
class Circle(Element):
    def __init__(self, ctr, r, **attrs):
        Element.__init__(self,
            cx=ctr[0], cy=ctr[1], r=r, **attrs)

@adder
@register('ellipse', 'styled')
class Ellipse(Element):
    def __init__(self, ctr, rx, ry, **attrs):
        Element.__init__(self,
            cx=ctr[0], cy=ctr[1], rx=rx, ry=ry, **attrs)

@adder
@register('text', 'styled')
class Text(Element):
    def __init__(self, pt, text, **attrs):
        Element.__init__(self, x=pt[0], y=pt[1], **attrs)
        self.add(text)
