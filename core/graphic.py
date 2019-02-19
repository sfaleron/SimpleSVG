
from __future__ import absolute_import

from .base import Element, Style, registry

from .path import Path
from .util import pairsfmt, unexpression_adder


__all__, adder = unexpression_adder(['Path'])

@adder
@registry.add('polygon', 'styled')
class Polygon(Element):
    def __init__(self, pts, **attrs):
        Element.__init__(self, points=pairsfmt(pts), **attrs)

@adder
@registry.add('polyline', 'styled')
class PolyLine(Element):
    def __init__(self, pts, **attrs):
        Element.__init__(self, points=pairsfmt(pts), **attrs)

@adder
def filled_polygon(pts, fillColor, **attrs):
    return Polygon(pts, fill=fillColor, **attrs)


@adder
@registry.add('line', 'styled')
class Line(Element):
    def __init__(self, pt1, pt2, **attrs):
        Element.__init__(self,
            x1=pt1[0], y1=pt1[1], x2=pt2[0], y2=pt2[1], **attrs)

@adder
@registry.add('rect', 'styled')
class Rect(Element):
    def __init__(self, pt, w, h, rx='0', ry='0', **attrs):
        Element.__init__(self,
            x=pt[0], y=pt[1], width=w, height=h, rx=rx, ry=ry, **attrs)

@adder
@registry.add('circle', 'styled')
class Circle(Element):
    def __init__(self, ctr, r, **attrs):
        Element.__init__(self,
            cx=ctr[0], cy=ctr[1], r=r, **attrs)

@adder
@registry.add('ellipse', 'styled')
class Ellipse(Element):
    def __init__(self, ctr, rx, ry, **attrs):
        Element.__init__(self,
            cx=ctr[0], cy=ctr[1], rx=rx, ry=ry, **attrs)

@adder
@registry.add('text', 'styled')
class Text(Element):
    def __init__(self, pt, text='', **attrs):
        Element.__init__(self, x=pt[0], y=pt[1], **attrs)
        if text:
            self.add(text)
