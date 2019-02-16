
from  __future__   import division
from  __future__   import print_function
from  __future__   import absolute_import

from itertools     import product
from math          import sin, cos, pi

from simplesvg     import SVGStack, SVG, Polygon
from simplesvg.lib import ArcDecorations, TickDecorations

from simplesvg.lib.math import Point, make_scaler

SCL =  200
OFF = pi/8
N   =    6

o = Point(1.15, 1.15)

Scale = make_scaler(SCL)


if __name__ == '__main__':
    pgonAttrs = {'stroke-width': Scale(.01).px,   'stroke': '#0000ff', 'fill-opacity': 0}
    decAttrs  = {'stroke-width': Scale(.0035).px, 'stroke': '#0000ff'}

    stk   = SVGStack(SVG('Congruency Decorations', width=Scale(2.3), height=Scale(2.3)))

    arcs  =  ArcDecorations(radius=Scale(.05), spacing=Scale(.015))
    ticks = TickDecorations(length=Scale(.08), spacing=Scale(.02))

    pts = [SCL*(Point(cos(a), sin(a))+o) for a in [2*pi/N*i+OFF for i in range(N)]]
    stk.add(Polygon(pts, **pgonAttrs))

    for i in range(N):
        stk.add(ticks(pts[i], pts[(i+1)%N], i+1, **decAttrs))
        stk.add(arcs( pts[i], pts[(i-1)%N], pts[(i+1)%N], i&1, i+1, **decAttrs))

    print(stk)
