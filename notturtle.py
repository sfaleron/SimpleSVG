
# SVG's coordinate system has an inverted y-axis from the conventional
# cartesian coordinate system used outside computer graphics:
# positive y is down, increasing angles go clockwise, the quadrants are
# flipped about the x-axis.

from simplesvg import Path

UP, DOWN, LEFT, RIGHT = range(4)

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


   def _quadrant(self, whichway, r):
      orientation, sgnx, sgny, incAngle = TURNS[(self._orientation, whichway)]

      self.arcTo((sgnx*r, sgny*r), r, r, 0, False, incAngle)

      self._orientation = orientation

   def turnLeft(self, r):
      self._quadrant(LEFT, r)

   def turnRight(self, r):
      self._quadrant(RIGHT, r)

   def forward(self, howFar):
      self.lineTo( {
         UP:    (0, -howFar),
         DOWN:  (0,  howFar),
         LEFT:  (-howFar, 0),
         RIGHT: ( howFar, 0)
      }[ self._orientation])

if __name__ == '__main__':
   from simplesvg import SVGStack
   from itertools import product

   stk = SVGStack()
   for i, j in product((UP, DOWN, LEFT, RIGHT), (LEFT, RIGHT)):
      #ni =
      pass
