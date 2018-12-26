
from __future__ import absolute_import

from  simplesvg import SVGStack, filled_polygon

from    .layers import layerReg
from   .options import opts


class Canvas(SVGStack):
    pass


def make_svg(args=()):
    if 'swap' in args:
        opts.slim, opts.squat = opts.squat, opts.slim
        args.remove('swap')

    stk = SVGStack()

    layerReg['background'](stk, opts.tri1, opts.bg, **opts.attrs.pgon)


    label, color = ('slim', opts.slim) if opts.flip else ('squat', opts.squat)

    stk.push_layer(label, True)

    stk.add(filled_polygon(opts.tri('A','F','H'), color, **opts.attrs.pgon))
    stk.add(filled_polygon(opts.tri('B','D','I'), color, **opts.attrs.pgon))
    stk.add(filled_polygon(opts.tri('C','E','G'), color, **opts.attrs.pgon))

    stk.pop()

    label, color = ('squat', opts.squat) if opts.flip else ('slim', opts.slim)

    stk.push_layer(label, True)

    stk.add(filled_polygon(opts.tri('A','E','H'), color, **opts.attrs.pgon))
    stk.add(filled_polygon(opts.tri('B','F','I'), color, **opts.attrs.pgon))
    stk.add(filled_polygon(opts.tri('C','D','G'), color, **opts.attrs.pgon))

    stk.pop()

    layerReg['ctrsq'](stk, opts.tri2, opts.squat, **opts.attrs.pgon)
    layerReg['ctrsl'](stk, opts.tri2, opts.slim, **opts.attrs.pgon)
    layerReg['ctrbg'](stk, opts.tri2, opts.bg, **opts.attrs.pgon)

    layerReg['rays'](stk, opts.tri1, opts.tri3, opts.flip, **opts.attrs.line)

    layerReg['glyph'](stk)

    layerReg['labels'](stk, opts.labels, opts.points, opts.size)


    if args:
        for layer in stk.layers:
            layer.visible = layer.label in args

    return stk
