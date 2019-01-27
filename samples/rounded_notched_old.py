
from __future__ import print_function

"""Constructs a rounded-rectangle path with an inset space on the
(presumably) short side, as might be used to prevent a looping
attachment from slipping off.

This is the older version, using only the quadrant API.
"""

from simplesvg import SVG

from simplesvg.lib import Quadrant

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

    doc  = SVG('Rounded and Notched Rectangle, Old: Quadrant API')

    path = doc.add(Quadrant(**attrs))

    path.quadrant( 2, RADIUS)

    if WIDER:
        path.rel.lineTo((WIDER, 0.0))

    path.quadrant( 1, RADIUS)
    path.quadrant( 3, RADIUS, incAngle=False)

    path.rel.lineTo((GAP, 0.0))

    path.quadrant( 4, RADIUS, incAngle=False)
    path.quadrant( 2, RADIUS)

    if WIDER:
        path.rel.lineTo((WIDER, 0.0))

    path.quadrant( 1, RADIUS)
    path.rel.lineTo((0.0, STRAIGHT_SIDE))

    path.quadrant( 4, RADIUS)

    if WIDER:
        path.rel.lineTo((-WIDER, 0.0))

    path.quadrant( 3, RADIUS)
    path.quadrant( 1, RADIUS, incAngle=False)

    path.rel.lineTo((-GAP, 0.0))

    path.quadrant( 2, RADIUS, incAngle=False)
    path.quadrant( 4, RADIUS)

    if WIDER:
        path.rel.lineTo((-WIDER, 0.0))

    path.quadrant( 3, RADIUS)

    path.close()

    print(doc)
