
from  __future__   import division
from  __future__   import print_function
from  __future__   import absolute_import

from itertools     import product

from simplesvg     import SVGStack, Path, Line
from simplesvg.lib import make_decorations
from simplesvg.lib.math import Point

o = Point(1.15, 1.15)

if __name__ == '__main__':
    lineAttrs = {'stroke-width' :   '.01px', 'stroke': '#0000ff'}
    decAttrs  = {'stroke-width' : '.0035px', 'stroke': '#0000ff', 'fill-opacity':0}

    stk  = SVGStack(width=2.3, height=2.3)
    ticks, arcs = make_decorations(tickLength=0.1, arcRadius=0.05, spacing=0.02)

    pts = [Point(*i)+o for i in ((-1,1),(-1,-1),(1,-1),(1,1))]

    for i in range(4):
        stk.add(Line( pts[i], pts[(i+1)%4], **lineAttrs))
        stk.add(ticks(pts[i], pts[(i+1)%4], i+1, **decAttrs))
        stk.add(arcs( pts[i], pts[(i-1)%4], pts[(i+1)%4], False, i+1, **decAttrs))

    print(stk)
