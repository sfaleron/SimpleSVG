
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from  simplesvg import SVGStack
from     triphi import layerReg, defaults

class FancySet(set):
    def __init__(self, regmap):
        self._regmap = regmap

    def __getitem__(self, key):
        if key in self:
            return self._regmap[key]
        else:
            return lambda *args, **kw: None


def make_svg(args=(), opts=None):
    if opts is None:
        opts = defaults

    opts     = opts.copy()
    colors   = opts.colors
    layers   = FancySet(layerReg)

    purgeInvisible = False

    for i,j in reversed(tuple(enumerate(args))):
        if j.startswith(':'):
            x = j.split(':')
            cmd   = x[ 1]
            parms = x[2:]

            if cmd == 'swap':
                colors.slim, colors.squat = colors.squat, colors.slim

            if cmd == 'purge':
                purgeInvisible = True

            if cmd == 'flip':
                opts.flip = not opts.flip

            if cmd == 'rot':
                opts.rot = float(parms[0])/180*pi

            if cmd == 'side':
                opts.side = float(parms[0])

            # +/- layers (from defaults?)
            # toggle/on/off visibility
            # show layers/visibility

        else:
            layers.add(j)

    if not layers:
        layers.update(layerReg.names)

    _,_, w,h = opts.geo

    stk = SVGStack(width=w, height=h)

    layers['background'](stk, opts.tri1, colors.bg, **opts.attrs.pgon)

    layers['slim'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layers['squat'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layers['ctrsq'](stk, opts.tri2, colors.squat, **opts.attrs.pgon)
    layers['ctrsl'](stk, opts.tri2, colors.slim, **opts.attrs.pgon)
    layers['ctrbg'](stk, opts.tri2, colors.bg, **opts.attrs.pgon)

    layers['rays'](stk, opts.tri1, opts.tri3, opts.flip, **opts.attrs.line)

    layers['glyph'](stk, opts.side, opts.center)

    layers['labels'](stk, opts.labels, opts.points, opts.side)


    if args:
        for layer in stk.layers:
            layer.visible = layer.label in args

    if purgeInvisible:
        stk.purge_invisible_layers()

    return stk

if __name__ == '__main__':
    import sys

    print(make_svg(sys.argv[1:]))
