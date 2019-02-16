
from __future__ import print_function

"""Constructs a rounded-rectangle path with an inset space on the
(presumably) short side, as might be used to prevent a looping
binding from slipping off.

This is the newer version, using the NotTurtle API.
"""

from simplesvg import SVG

from simplesvg.lib import NotTurtle

if __name__ == '__main__':
    GAP    = 4.5
    WIDER  = 1.5
    RADIUS = 1.5
    STRAIGHT_SIDE = 28.4

    # stroke-width = 0.01px for an actual Ponoko submission,
    # but that is basically invisible when rendered on-screen.
    attrs = {
        'stroke'        : '#0000ff',
        'stroke-width'  : '0.1px',
        'stroke-opacity': 1,
        'fill-opacity'  : 0
    }

    doc  = SVG('Rounded and Notched Rectangle, New: NotTurtle API')
    path = doc.add(NotTurtle(**attrs))

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
