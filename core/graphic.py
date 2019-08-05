
from __future__ import absolute_import

from .base import StyledElement

from .path import Path
from .util import pairsfmt, unexpression_adder


__all__, adder = unexpression_adder(['Path'])

@adder
class Polygon(StyledElement):
    def __init__(self, pts, **attrs):
        StyledElement.__init__(self, 'polygon', points=pairsfmt(pts), **attrs)

@adder
class PolyLine(StyledElement):
    def __init__(self, pts, **attrs):
        StyledElement.__init__(self, 'polyline', points=pairsfmt(pts), **attrs)

@adder
def filled_polygon(pts, fillColor, **attrs):
    return Polygon(pts, fill=fillColor, **attrs)


@adder
class Line(StyledElement):
    def __init__(self, pt1, pt2, **attrs):
        StyledElement.__init__(self, 'line',
            x1=pt1[0], y1=pt1[1], x2=pt2[0], y2=pt2[1], **attrs)

@adder
class Rect(StyledElement):
    def __init__(self, pt, w, h, rx='0', ry='0', **attrs):
        StyledElement.__init__(self, 'rect',
            x=pt[0], y=pt[1], width=w, height=h, rx=rx, ry=ry, **attrs)

@adder
class Circle(StyledElement):
    def __init__(self, ctr, r, **attrs):
        StyledElement.__init__(self, 'circle',
            cx=ctr[0], cy=ctr[1], r=r, **attrs)

@adder
class Ellipse(StyledElement):
    def __init__(self, ctr, rx, ry, **attrs):
        StyledElement.__init__(self, 'ellipse',
            cx=ctr[0], cy=ctr[1], rx=rx, ry=ry, **attrs)

@adder
class Text(StyledElement):
    def __init__(self, pt, text='', **attrs):
        StyledElement.__init__(self, 'text', x=pt[0], y=pt[1], **attrs)
        self.delimiter = ''
        if text:
            self.add(text)

    def set_root(self, e):
        StyledElement.set_root(self, e)
        if 'inkOffsetFix' in e.docFlags:
            self.update(
                x=float(self['x'])+float(self.pop('dx', '0')),
                y=float(self['y'])+float(self.pop('dy', '0')) )
