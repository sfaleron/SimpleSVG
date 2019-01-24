
from  __future__   import division
from  __future__   import print_function
from  __future__   import absolute_import

from itertools     import product

from simplesvg     import SVGStack, SVG, Polygon
from simplesvg.lib import ArcDecorations, TickDecorations

from simplesvg.lib.math import Point

from math import sin,cos,pi

SCL =  200
OFF = pi/8
N   =    6

o = Point(1.15, 1.15)


if __name__ == '__main__':
    pgonAttrs = {'stroke-width' : '{:f}px'.format(.01 * SCL), 'stroke': '#0000ff', 'fill-opacity':0}
    decAttrs  = {'stroke-width' : '{:f}px'.format(.0035*SCL), 'stroke': '#0000ff'}

    stk   = SVGStack(SVG('Congruency Decorations', width=2.3*SCL, height=2.3*SCL))

    arcs  =  ArcDecorations(radius=0.05*SCL, spacing=0.015*SCL)
    ticks = TickDecorations(length=0.08*SCL, spacing=0.02 *SCL)

    pts = [SCL*(Point(cos(a), sin(a))+o) for a in [2*pi/N*i+OFF for i in range(N)]]
    stk.add(Polygon(pts, **pgonAttrs))

    for i in range(N):
        stk.add(ticks(pts[i], pts[(i+1)%N], i+1, **decAttrs))
        stk.add(arcs( pts[i], pts[(i-1)%N], pts[(i+1)%N], i&1, i+1, **decAttrs))

    print(stk)
