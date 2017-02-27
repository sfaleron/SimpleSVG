
from simplesvg import Path

UP, DOWN, LEFT, RIGHT = range(4)
I, II, III, IV = range(4)

SIGNS = {
   'x': (-1, -1, 1, 1),
   'y': ( 1, -1,-1, 1)
}

TURNS = {
   UP:    { LEFT: (  I,  LEFT), RIGHT: ( II, RIGHT) },
   DOWN:  { LEFT: (III, RIGHT), RIGHT: ( IV,  LEFT) },
   LEFT:  { LEFT: ( II,  DOWN), RIGHT: (III,    UP) },
   RIGHT: { LEFT: ( IV,    UP), RIGHT: (  I,  DOWN) }
}


# merely inspired-by
class NotTurtle(Path):
   def __init__(self, initial_pos=(0,0), **attrs):
      Path.__init__(self, initial_pos, **attrs)
      self._orientation = UP

   def quadrant(self, quadrant, r, incAngle=True, flipY=True):
   
      dx = r * SIGNS['x'][quadrant]
      dy = r * SIGNS['y'][quadrant]
   
      if flipY:
         dy *= -1
   
      if incAngle:
         dx *= -1
         dy *= -1
   
      self.arcTo((dx, dy), r, r, 0, False, incAngle)

   def turnLeft(self, r):
      q, newOrientation = TURNS[self._orientation][LEFT]
      self._orientation = newOrientation
      self.quadrant(q, r, False)

   def turnRight(self, r):
      q, newOrientation = TURNS[self._orientation][RIGHT]
      self._orientation = newOrientation
      self.quadrant(q, r, True)

   def forwards(self, howFar):
      self.lineTo( {
         UP:    (0, -howFar),
         DOWN:  (0,  howFar),
         LEFT:  (-howFar, 0),
         RIGHT: ( howFar, 0)
      }[ self._orientation])
