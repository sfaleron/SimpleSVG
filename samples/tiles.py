
from __future__ import print_function
from __future__ import absolute_import

from  simplesvg import SVGStack
from     triphi import *

def make_tile(stk, opts):
    layerReg['slim'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['squat'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['ctrbg'](stk, opts.tri2, colors.bg, **opts.attrs.pgon)

def make_tiles(n, opts=None):
    if opts is None:
        opts = defaults.copy()

    stk = SVGStack()

    return stk

if __name__ == '__main__':
    import sys

    print(make_tiles(int(sys.argv[1])))
