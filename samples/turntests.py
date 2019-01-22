
from simplesvg.lib.rtangles import UP, DOWN, LEFT, RIGHT
from simplesvg.lib import RoundedRect, NotTurtle
from simplesvg     import SVGStack, Line

from itertools     import product

attrs = {
    'stroke'        : '#0000ff',
    'stroke-width'  : 0.5,
    'stroke-opacity': 1,
    'fill-opacity'  : 0
}

if __name__ == '__main__':
    stk = SVGStack(transform='translate(100 80)')

    stk.push_layer('rounded rectangles')

    stk.add(RoundedRect(  2e2,   1e2, 1e1, **attrs))

    stk.add(RoundedRect(1.5e2,   2e1, 1e1, **attrs))

    stk.add(RoundedRect(  2e1, 1.5e2, 1e1, **attrs))

    stk.add(RoundedRect(  2e1,   2e1, 1e1, (20, 60), **attrs))

    stk.add(RoundedRect(  4e1, 2.5e1, {'ul':0, 'll':5, 'lr':10, 'ur':15}, (-40, 70), **attrs))

    stk.add(Line((-65, 70), (-15, 70), **attrs))
    stk.add(Line((-40, 52.5), (-40, 87.5), **attrs))

    stk.pop()

    for i, j in product((UP, DOWN, LEFT, RIGHT), (LEFT, RIGHT)):
        stk.push_layer('%s then %s' % ({UP: 'up', DOWN:'down', RIGHT: 'right', LEFT:'left'}[i], {LEFT:'left',RIGHT: 'right'}[j]))
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