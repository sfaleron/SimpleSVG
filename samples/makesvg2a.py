
from __future__ import print_function

"""Constructs a rounded-rectangle path with an inset space on the
(presumably) short side, as might be used to prevent a looping
attachment from slipping off.

This is the older version, using only the quadrant API.
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
    path = doc.add_child(NotTurtle((0, 0),
        **{'stroke-width':str(STROKE_WIDTH), 'stroke':'#0000ff',
            'stroke-opacity':'1', 'fill-opacity':'0'}))

    path.quadrant(1, RADIUS)

    if WIDER:
        path.lineTo((WIDER, 0.0))

    path.quadrant(0, RADIUS)
    path.quadrant(2, RADIUS, incAngle=False)

    path.lineTo((GAP, 0.0))

    path.quadrant(3, RADIUS, incAngle=False)
    path.quadrant(1, RADIUS)

    if WIDER:
        path.lineTo((WIDER, 0.0))

    path.quadrant(0, RADIUS)
    path.lineTo((0.0, STRAIGHT_SIDE))

    path.quadrant(3, RADIUS)

    if WIDER:
        path.lineTo((-WIDER, 0.0))

    path.quadrant( 2, RADIUS)
    path.quadrant(0, RADIUS, incAngle=False)

    path.lineTo((-GAP, 0.0))

    path.quadrant(1, RADIUS, incAngle=False)
    path.quadrant(3, RADIUS)

    if WIDER:
        path.lineTo((-WIDER, 0.0))

    path.quadrant(2, RADIUS)

    path.close()

    print(doc)
