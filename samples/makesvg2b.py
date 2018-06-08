
from __future__ import print_function

"""Constructs a rounded-rectangle path with an inset space on the
(presumably) short side, as might be used to prevent a looping
attachment from slipping off.

This is the newer version, using the NotTurtle API.
"""

from simplesvg import SVG

from simplesvg.notturtle import *

if __name__ == '__main__':
    GAP    = 4.5
    WIDER  = 1.5
    RADIUS = 1.5
    STROKE_WIDTH  = 0.01
    STRAIGHT_SIDE = 28.4

    doc = SVG()
    path = doc.add_child(NotTurtle(
        **{'stroke-width':str(STROKE_WIDTH), 'stroke':'#0000ff',
            'stroke-opacity':'1', 'fill-opacity':'0'}))

    path.turnRight(RADIUS)

    if WIDER:
        path.forwards(WIDER)

    path.turnRight(RADIUS)
    path.turnLeft( RADIUS)

    path.forwards(GAP)

    path.turnLeft( RADIUS)
    path.turnRight(RADIUS)

    if WIDER:
        path.forwards(WIDER)

    path.turnRight(RADIUS)
    path.forwards(STRAIGHT_SIDE)

    path.turnRight(RADIUS)

    if WIDER:
        path.forwards(WIDER)

    path.turnRight(RADIUS)
    path.turnLeft( RADIUS)

    path.forwards(GAP)

    path.turnLeft( RADIUS)
    path.turnRight(RADIUS)

    if WIDER:
        path.forwards(WIDER)

    path.turnRight(RADIUS)

    path.close()

    print(doc)
