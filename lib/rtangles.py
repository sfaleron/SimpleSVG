
# SVG's coordinate system has an inverted y-axis from the conventional
# cartesian coordinate system used outside computer graphics:
# positive y is down, increasing angles go clockwise, the quadrants are
# flipped about the x-axis.

from __future__ import division

from  simplesvg import Path

from       enum import Enum

Dir = Enum('Dir', 'UP DOWN LEFT RIGHT')

UP, DOWN, LEFT, RIGHT = Dir.__members__.values()


# new orientation, signs of dx/dy, clockwise/increasing angle?
TURNS = {
    (   UP,  LEFT): ( LEFT, -1, -1, False),
    (   UP, RIGHT): (RIGHT,  1, -1,  True),
    ( DOWN,  LEFT): (RIGHT,  1,  1, False),
    ( DOWN, RIGHT): ( LEFT, -1,  1,  True),
    ( LEFT,  LEFT): ( DOWN, -1,  1, False),
    ( LEFT, RIGHT): (   UP, -1, -1,  True),
    (RIGHT,  LEFT): (   UP,  1, -1, False),
    (RIGHT, RIGHT): ( DOWN,  1,  1,  True)
}

# merely inspired-by
class NotTurtle(Path):
    def __init__(self, initial_pos=(0,0), initial_orientation=UP, **attrs):
        Path.__init__(self, initial_pos, **attrs)
        self._orientation = initial_orientation

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        if val in (UP, DOWN, LEFT, RIGHT):
            self._orientation = val
        else:
            raise ValueError('not a valid orientation')

    def _doTurn(self, whichway, r):
        orientation, sgnx, sgny, incAngle = TURNS[(self._orientation, whichway)]

        if r:
            self.arcTo((sgnx*r, sgny*r), r, r, 0, False, incAngle)

        self._orientation = orientation

    def turnLeft(self, r):
        self._doTurn(LEFT, r)

    def turnRight(self, r):
        self._doTurn(RIGHT, r)

    def forward(self, howFar):
        self.lineTo( {
            UP:    (0, -howFar),
            DOWN:  (0,  howFar),
            LEFT:  (-howFar, 0),
            RIGHT: ( howFar, 0)
        }[ self._orientation])


from collections import Mapping

def RoundedRect(w, h, r, pos=(0.0, 0.0), **attrs):
    CORNERS = ('ul', 'll', 'lr', 'ur')
    STROKE_WIDTH = 1.0
    EPSILON = 1e-6

    w = float(w)
    h = float(h)

    pos = tuple(map(float, pos))

    if not isinstance(r, Mapping):
        r = dict(ul=r, ur=r, ll=r, lr=r)

    path = NotTurtle( (pos[0]-w/2, pos[1]-h/2+r['ul']), DOWN, **attrs )

    for i in range(4):
        d = w if i&1 else h

        r1 = r[CORNERS[i]]
        r2 = r[CORNERS[(i+1)%4]]

        if (d-r1-r2) > EPSILON:
            path.forward(d-r1-r2)

        path.turnLeft(r2)

    return path


SIGNS = {
    'x': (-1, -1, 1, 1),
    'y': ( 1, -1,-1, 1)
}

class Quadrant(Path):
    def __init__(self, initial_pos=(0,0), **attrs):
        Path.__init__(self, initial_pos, **attrs)

    def quadrant(self, quadrant, r, incAngle=True, flipY=True):
        dx = r * SIGNS['x'][quadrant-1]
        dy = r * SIGNS['y'][quadrant-1]

        if flipY:
            dy *= -1

        if incAngle:
            dx *= -1
            dy *= -1

        self.arcTo((dx, dy), r, r, 0, False, incAngle)


__all__ = ('NotTurtle', 'RoundedRect', 'Quadrant', 'Dir')
