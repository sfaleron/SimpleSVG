
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
    STRAIGHT_SIDE = 28.4

    attrs = {
        'stroke'        : '#0000ff',
        'stroke-width'  : 0.01,
        'stroke-opacity': 1,
        'fill-opacity'  : 0
    }

    doc = SVG()
    path = doc.add_child(NotTurtle(**attrs))

    path.turnRight(RADIUS)

    if WIDER:
        path.forward(WIDER)

    path.turnRight(RADIUS)
    path.turnLeft( RADIUS)

    path.forward(GAP)

    path.turnLeft( RADIUS)
    path.turnRight(RADIUS)

    if WIDER:
        path.forward(WIDER)

    path.turnRight(RADIUS)
    path.forward(STRAIGHT_SIDE)

    path.turnRight(RADIUS)

    if WIDER:
        path.forward(WIDER)

    path.turnRight(RADIUS)
    path.turnLeft( RADIUS)

    path.forward(GAP)

    path.turnLeft( RADIUS)
    path.turnRight(RADIUS)

    if WIDER:
        path.forward(WIDER)

    path.turnRight(RADIUS)

    path.close()

    print(doc)
