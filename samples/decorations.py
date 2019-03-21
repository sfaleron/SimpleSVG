
from  __future__   import division
from  __future__   import print_function
from  __future__   import absolute_import

from itertools     import product

from simplesvg     import SVGStack, SVG, Polygon
from simplesvg.lib import ArcDecorations, HatchDecorations, CornerDecorations, LineLabel

from simplesvg.lib.math import Point, make_scaler, midpoint, sin, cos, pi

SCL =  200
OFF = pi/8
N   =    6

o = Point(1.15, 1.15)

Scale = make_scaler(SCL)

labels = ('label one', 'label two', 'label three', 'label four', 'label five', 'label six')

if __name__ == '__main__':
    pgonAttrs = {'stroke-width': Scale(.01).px,   'stroke': '#0000ff', 'fill-opacity': 0}
    decAttrs  = {'stroke-width': Scale(.0035).px, 'stroke': '#0000ff', 'font-size': '65%', 'font-weight': 'lighter'}

    stk     = SVGStack(SVG('Congruency Decorations', width=Scale(2.3), height=Scale(2.3)))

    arcs    =    ArcDecorations(   radius=Scale(.05), spacing=Scale(.0125))
    hatches =  HatchDecorations(   length=Scale(.08), spacing=Scale(.0160))
    corners = CornerDecorations(legLength=Scale(.05), spacing=Scale(.0125))

    pts = [SCL*(Point(cos(a), sin(a))+o) for a in [2*pi/N*i+OFF for i in range(N)]]
    stk.add(Polygon(pts, **pgonAttrs))

    for i in range(N):
        midPt = midpoint(pts[i], pts[(i+1)%N])
        stk.add(LineLabel(pts[i], pts[(i+1)%N], labels[i], i&1, dy=Scale(-.08), **decAttrs))

        stk.add(hatches(pts[i], pts[(i+1)%N], i+1, **decAttrs))
        stk.add(arcs(   pts[i], pts[(i-1)%N], pts[(i+1)%N], i&1, i+1, **decAttrs))
        stk.add(corners(pts[i], pts[(i-1)%N], pts[(i+1)%N], not i&1, i+1, **decAttrs))

    print(stk)
