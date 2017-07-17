
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

      if r:
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


from collections import Mapping

def RoundedRect(w, h, r, pos=(0.0, 0.0), **attrs):
   CORNERS = ('ul', 'll', 'lr', 'ur')
   STROKE_WIDTH = 1.0
   EPSILON = 1e-6

   w = float(w)
   h = float(h)

   pos = map(float, pos)

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


if __name__ == '__main__':
   #from simplesvg import EmbedStack, Line
   from simplesvg import SVGStack, Line
   from itertools import product

   attrs = {
      'stroke-width':'0.5', 'stroke':'#0000ff',
      'stroke-opacity':'1', 'fill-opacity':'0'}

   #stk = EmbedStack()
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

   print stk
