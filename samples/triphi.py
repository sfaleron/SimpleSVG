
from __future__ import print_function
from __future__ import absolute_import

from  simplesvg import SVGStack
from     triphi import *


def make_svg(args=(), opts=None):
    if opts is None:
        opts = defaults.copy()

    colors = opts.colors

    if 'swap' in args:
        args.remove('swap')
        colors.slim, colors.squat = colors.squat, colors.slim

    purgeInvisible = 'purge' in args

    if purgeInvisible:
        args.remove('purge')

    stk = SVGStack()

    layerReg['background'](stk, opts.tri1, colors.bg, **opts.attrs.pgon)

    layerReg['slim'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['squat'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['ctrsq'](stk, opts.tri2, colors.squat, **opts.attrs.pgon)
    layerReg['ctrsl'](stk, opts.tri2, colors.slim, **opts.attrs.pgon)
    layerReg['ctrbg'](stk, opts.tri2, colors.bg, **opts.attrs.pgon)

    layerReg['rays'](stk, opts.tri1, opts.tri3, opts.flip, **opts.attrs.line)

    layerReg['glyph'](stk)

    layerReg['labels'](stk, opts.labels, opts.points, opts.side)


    if args:
        for layer in stk.layers:
            layer.visible = layer.label in args

    if purgeInvisible:
        stk.purge_invisible_layers()

    return stk

if __name__ == '__main__':
    import sys

    print(make_svg(sys.argv[1:]))
