
# Prints out all nine vertices given the standard side length,
# original center and recentered on the origin, both flipped
# and unflipped. Useful for comparisons/validation.

from __future__     import print_function
from __future__     import absolute_import, division

from triphi.math    import inner, outer, Point
from triphi.options import standardSide


def mkdumpfunc(lw, rw):
    fmtstr = ' '.join([','.join(['%%%d.%df' % (lw+rw+1, rw)]*2)]*3)
    return lambda p1, p2, p3: fmtstr % (p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)

if __name__ == '__main__':

    dumpfunc     = mkdumpfunc(4, 4)

    A,B,C        = outer(standardSide)

    center       = Point(*[sum(i)/3 for i in zip(A,B,C)])

    centered     = [Point(pt.x-center.x, pt.y-center.y) for pt in (A,B,C)]

    print('Center:', center)

    print('ABC', dumpfunc(A,B,C))

    D,E,F, G,H,I = inner(A,B,C, False)

    print('DEF', dumpfunc(D,E,F), 'no flip')
    print('GHI', dumpfunc(G,H,I))

    D,E,F, G,H,I = inner(A,B,C, True)

    print('DEF', dumpfunc(D,E,F), 'flipped')
    print('GHI', dumpfunc(G,H,I))


    print('Center:', Point(0,0))

    A,B,C        = centered

    print('ABC', dumpfunc(A,B,C))

    D,E,F, G,H,I = inner(A,B,C, False)

    print('DEF', dumpfunc(D,E,F), 'no flip')
    print('GHI', dumpfunc(G,H,I))

    D,E,F, G,H,I = inner(A,B,C, True)

    print('DEF', dumpfunc(D,E,F), 'flipped')
    print('GHI', dumpfunc(G,H,I))
