
from __future__ import print_function

from simplesvg.lib.dirs import *
from simplesvg.lib      import RoundedRect, NotTurtle
from simplesvg          import SVGStack, Line, SVG

from itertools          import product

CLRS  = (
    '#B400FF', '#E60000', '#FFC600',
    '#FFED00', '#BEFF00', '#00FF52',
    '#00FFD2', '#00B2FF', '#0073FF' )


attrs = {
    'stroke'        : CLRS[0],
    'stroke-width'  : '1px',
    'stroke-opacity': 1,
    'fill-opacity'  : 0
}

if __name__ == '__main__':
    stk = SVGStack(SVG('Rounded Rectangle Test and Demonstration', width=365, height=185))

    stk.push_layer('rounded rectangles', visible=True, transform='translate(110 85)')

    stk.add(RoundedRect(  2e2,   1e2, 1e1, **attrs))

    stk.add(RoundedRect(1.5e2,   2e1, 1e1, **attrs))

    stk.add(RoundedRect(  2e1, 1.5e2, 1e1, **attrs))

    stk.add(RoundedRect(  2e1,   2e1, 1e1, (20, 60), **attrs))

    stk.add(RoundedRect(  4e1, 2.5e1, {'ul':0, 'll':5, 'lr':10, 'ur':15}, (-40, 70), **attrs))

    stk.add(Line((-65, 70), (-15, 70), **attrs))
    stk.add(Line((-40, 52.5), (-40, 87.5), **attrs))

    stk.pop()

    for i,j,k in [ii+(jj,) for ii,jj in zip(
        product([UP, DOWN, LEFT, RIGHT], [LEFT, RIGHT]), CLRS[1:])]:
        stk.push_layer('{} then {}'.format(DIRTXT[i], DIRTXT[j]), visible=True, transform='translate(195 -15)')

        attrs.update(stroke=k)
        path = NotTurtle((100, 100), i, **attrs)

        path.forward(50)

        if j == LEFT:
            path.turnLeft(10)
        else:
            path.turnRight(10)

        path.forward(40)

        stk.add(path)
        stk.pop()

    print(stk)
