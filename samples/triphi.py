
from math import sin, cos, pi

from collections import namedtuple

# for an SVG canvas
def transform(p):
   return Point(SIDE + p.x, SIDE - p.y)

Point = namedtuple('Point', ('x', 'y'))


SIDE = 400.0

# Construct a figure like that at http://www.cut-the-knot.org/do_you_know/Buratino7.shtml
# our points are labeled counterclockwise, which doesn't always correspond to the diagram on this page

# Concerning the proof on that page: it is terse, and at best misleading, I
# would say incorrect, but I am not accustomed to judging geometric proofs.
# Here is a clearer, correct proof, using their labels:

# AF   MN   FN   BF
# -- = -- = -- = --
# BF   BN   AM   AB

# The first equality comes from Thales, as stated. The last equality is due to
# triangle similarity. The center equality took me a while to figure out, but
# is true because MN = FN and BN = AM. The equality of the proportions at the
# ends defines the golden ratio.

# The equivalence of the segments used in the center equality follows clearly
# from the symmetry of the figure, but full rigor might demand more. I am
# doubtful that the rigor presented here is less than what appears on the web
# page, however!

# The interior segments are also in the Golden Ratio. They form the remaining
# side of the similar triangles.

# Maybe later: http://www.cut-the-knot.org/do_you_know/Buratino2.shtml

# Not triangular, but also interesting: http://www.cut-the-knot.org/do_you_know/Buratino6.shtml

####################################
# first, find the outermost triangle

# the Law of Cosines says
# a^2 + b^2 - 2*a*b*cos(C) = c^2

# c is the subtended chord, and one side of the triangle
# a and b are radii, and C is 120 degrees. easy-peasy!

# 2*r^2 + r^2 = s^2
# sqrt(3)*r = s

r = SIDE*3**-2**-1

A,B,C = [transform(Point(r*cos(a), r*sin(a))) for a in [(2./3*i+.5)*pi for i in range(3)]]

########################################
# find the inner triangle, with vertices
# on the sides of the first triangle.

# D is colinear with AB, and the length of BD is the outermost side length AB divided by phi.

invphi = 2/(1+5**2**-1)

def between(p1, p2, pos):
   return Point((p1.x-p2.x)*pos+p2.x, (p1.y-p2.y)*pos+p2.y)


D = between(A, B, invphi)

E = between(B, C, invphi)

F = between(C, A, invphi)


# not so hard, right? the last three points are just
# the midpoints of the sides of the previous triangle.

def midpoint(p1, p2):
   return Point((p1.x+p2.x)/2, (p1.y+p2.y)/2)

G = midpoint(D, E)

H = midpoint(E, F)

I = midpoint(F, D)


def mkdumpfunc(lw, rw):
   fmtstr = ' '.join([','.join(['%%%d.%df' % (lw+rw+1, rw)]*2)]*3)
   return lambda p1, p2, p3: fmtstr % (p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)

if __name__ == '__main__':
   dumpfunc = mkdumpfunc(3, 4)

   print dumpfunc(A, B, C)
   print dumpfunc(D, E, F)
   print dumpfunc(G, H, I)
