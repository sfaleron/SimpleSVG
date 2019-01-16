
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

# Ptolemy's Theorem
# https://en.wikipedia.org/wiki/List_of_trigonometric_identities#Ptolemy's_theorem
#
# w+x, x+y = a,b;  z = 180-w-x-y
#
# a,b are givens, which parameterizes w,y,z by x.
#
# Find w,x,y,z such that
# (sin w)(sin y)  +  (sin x)(sin z) is in the form of a sum or difference trig formula:
# (sin a)(cos b) +/- (cos a)(sin b) or
# (sin a)(sin b) -/+ (cos a)(cos b).

from math import sin, cos, pi
from itertools import product

sin_ = lambda x: sin(x/180*pi)
cos_ = lambda x: cos(x/180*pi)

def cmp_(x, y):
    return abs(x-y)<1e-6

for x,a,b in product(range(-90, 90), repeat=3):
    z = x+75
    y = 60-x
    w = 45-x

    inValue  = sin_(w)*sin_(y) + sin_(x)*sin_(z)

    sinPlus  = sin_(a)*cos_(b) + cos_(a)*sin_(b)
    sinMinus = sin_(a)*cos_(b) - cos_(a)*sin_(b)

    cosPlus  = sin_(a)*sin_(b) - cos_(a)*cos_(b)
    cosMinus = sin_(a)*sin_(b) + cos_(a)*cos_(b)

    if cmp_(inValue, sinPlus):
        print('sin+', a, b, w, x, y, z)

    if cmp_(inValue, sinMinus):
        print('sin-', a, b, w, x, y, z)

    if cmp_(inValue, cosPlus):
        print('cos+', a, b, w, x, y, z)

    if cmp_(inValue, cosMinus):
        print('cos-', a, b, w, x, y, z)
