
# SVG's coordinate system has an inverted y-axis from the conventional
# cartesian coordinate system used outside computer graphics:
# positive y is down, increasing angles go clockwise, the quadrants are
# flipped about the x-axis.

from __future__ import division

from  simplesvg import Path
from          . import dirs as Dir

from .dirs import *

# IVY, clarification wanted ##
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

# Merely inspired-by
#
# Turtle, https://en.wikipedia.org/wiki/Turtle_graphics, is pretty simple.
# What's missing:
#   * Good location tracking
#   * Turns in angles other than multiples of ninety degrees
#   * Changing the color and width of the "pen"
#
# Either of the last two would require a fair bit of refactoring, but pen
# control (updating stroke and stroke-width) would require multiple Path
# objects, which becomes rather more dramatic.
#
# Location tracking is supported, but will likely diverge from what is
# rendered as the complexity increases.
#
class NotTurtle(Path):
    def __init__(self, initial_pos=(0,0), initial_orientation=UP, **attrs):
        Path.__init__(self, initial_pos, **attrs)
        self._orientation = initial_orientation
        self._location = list(initial_pos)
        self._drawing = True

    @property
    def location(self):
        return self._location

    @property
    def drawing(self):
        return self._drawing

    def pen_on(self):
        self._drawing = True

    def pen_off(self):
        self._drawing = False

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
            delta = (sgnx*r, sgny*r)

            if self._drawing:
                self.rel.arcTo( delta, r, r, 0, False, incAngle)
            else:
                self.rel.moveTo(delta)

            self._location[0] += delta[0]
            self._location[1] += delta[1]

        self._orientation  = orientation

    def turnLeft(self, r):
        self._doTurn(LEFT, r)

    def turnRight(self, r):
        self._doTurn(RIGHT, r)

    def forward(self, howFar):
        delta = {
            UP:    (0, -howFar),
            DOWN:  (0,  howFar),
            LEFT:  (-howFar, 0),
            RIGHT: ( howFar, 0)
        }[   self._orientation ]

        getattr(self.rel, 'lineTo' if self._drawing else 'moveTo')(delta)

        self._location[0] += delta[0]
        self._location[1] += delta[1]


from collections import Mapping

class MapOfLists(dict):
    def __setitem__(self, key, item):
        if key in self:
            self[key].append(item)
        else:
            dict.__setitem__(self, key, [item])

CORNERS = ('ul', 'll', 'lr', 'ur')
EPSILON = 1e-9

SIDES = MapOfLists()

for corner in CORNERS:
    SIDES[corner[0]+'_'] = corner
    SIDES['_'+corner[1]] = corner

def RoundedRect(w, h, r, pos=(0.0, 0.0), **attrs):
    w = float(w)
    h = float(h)

    pos = tuple(map(float, pos))

    if not isinstance(r, Mapping):
        r = dict(ul=r, ur=r, ll=r, lr=r)
    else:
        for side, corners in SIDES.items():
            if side in r:
                for corner in corners:
                    r[corner] = r[side]

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

        self.rel.arcTo((dx, dy), r, r, 0, False, incAngle)


__all__ = ('NotTurtle', 'RoundedRect', 'Quadrant', 'Dir')
