
from  __future__   import division
from  __future__   import print_function
from  __future__   import absolute_import

from itertools     import product

from simplesvg     import SVGStack, Path, Line
from simplesvg.lib import ArcDecorations, TickDecorations

from simplesvg.lib.math import Point

from math import sin,cos,pi

SCL =  200
OFF = pi/8
N   =    5

o = Point(1.15, 1.15)


if __name__ == '__main__':
    lineAttrs = {'stroke-width' : .01 * SCL, 'stroke': '#0000ff'}
    decAttrs  = {'stroke-width' : .0035*SCL, 'stroke': '#0000ff', 'fill-opacity':0}

    stk   = SVGStack(width=2.3*SCL, height=2.3*SCL)

    arcs  =  ArcDecorations(radius=0.05*SCL, spacing=0.015*SCL)
    ticks = TickDecorations(length=0.08*SCL, spacing=0.02 *SCL)

    pts = [SCL*(Point(cos(a), sin(a))+o) for a in [2*pi/N*i+OFF for i in range(N)]]

    for i in range(N):
        stk.add(Line( pts[i], pts[(i+1)%N], **lineAttrs))
        stk.add(ticks(pts[i], pts[(i+1)%N], i+1, **decAttrs))
        stk.add(arcs( pts[i], pts[(i-1)%N], pts[(i+1)%N], False, i+1, **decAttrs))

    print(stk)
