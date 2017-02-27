
DARK  = '#5c84d0'
LIGHT = '#acc8e4'
BG    = '#e0ecf8'

SLIM  = DARK
SQUAT = LIGHT

pathAttrs = dict(fill='none', stroke='black')
pathAttrs['stroke-width'] = '3px'

pgonAttrs = {'stroke-width' : '0', 'fill-opacity' : '1'}

lineAttrs = {'stroke' : 'black', 'stroke-width' : '3px'}


from triphi import A,B,C, D,E,F, G,H,I

from simplesvg import *

def make_svg(args=[]):
   global SLIM, SQUAT
   if 'swap' in args:
      SLIM, SQUAT = SQUAT, SLIM
      args.remove('swap')

   stk = SVGStack()

   stk.push_defs()

   stk.push_clip('trim')

   stk.add(Polygon((A,B,C)))

   stk.pop(); stk.pop()

   stk.push_layer('background', True)

   path = stk.add(filled_polygon((A,B,C), BG, **pgonAttrs))
   path['id'] = 'boundary'

   stk.pop()

   stk.push_layer('squat', True)

   stk.add(filled_polygon((A,D,I), SQUAT, **pgonAttrs))
   stk.add(filled_polygon((B,E,G), SQUAT, **pgonAttrs))
   stk.add(filled_polygon((C,F,H), SQUAT, **pgonAttrs))

   stk.pop()

   stk.push_layer('slim', True)

   stk.add(filled_polygon((A,F,I), SLIM, **pgonAttrs))
   stk.add(filled_polygon((B,D,G), SLIM, **pgonAttrs))
   stk.add(filled_polygon((C,E,H), SLIM, **pgonAttrs))

   stk.pop()

   stk.push_layer('ctrsl')

   stk.add(filled_polygon((D,E,F), SLIM, **pgonAttrs))

   stk.pop()

   stk.push_layer('ctrsq')

   stk.add(filled_polygon((D,E,F), SQUAT, **pgonAttrs))

   stk.pop()

   stk.push_layer('ctrbg')

   stk.add(filled_polygon((D,E,F), BG, **pgonAttrs))

   stk.pop()


   stk.push_layer('rays', True)
   g = stk.push_group('rays')
   g['clip-path'] = 'url(#trim)'

   stk.add(Line(A, H, **lineAttrs))
   stk.add(Line(B, I, **lineAttrs))
   stk.add(Line(C, G, **lineAttrs))

   stk.pop(); stk.pop()

   #stk.push_layer('reference')

   #stk.add(Circle(((A.x+B.x+C.x)/3,(A.y+B.y+C.y)/3),8, **{'stroke-width':'0'}))

   #stk.pop()


   stk.push_layer('glyph', True)

   stk.add(open('phiglyph.svg', 'r').read())

   stk.pop()

   if args:
      for layer in stk.layers:
         layer.visible = layer.label in args

   return stk


if __name__ == '__main__':
   import sys

   print str(make_svg(sys.argv[1:]))
