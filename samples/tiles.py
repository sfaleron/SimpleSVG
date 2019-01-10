
from __future__  import division
from __future__  import print_function
from __future__  import absolute_import

from simplesvg   import SVGStack, filled_polygon
from triphi      import defaults, redraw

from triphi.keyattr import KeywordToAttr
from triphi.layers  import mixed_up_triangles
from triphi.tiles   import TileSet, adjacent_tiles
from triphi.math    import inner


def make_tile(stk, path, opts):

    stk.push_layer('tile {}{}'.format(path, 'x' if opts.flip else '+'), True)

    mixed_up_triangles(stk,
        opts.tri1, opts.tri2, opts.tri3, opts.colors,
            opts.flip, name='squat', noLayer=True, **opts.attrs.pgon)

    mixed_up_triangles(stk,
        opts.tri1, opts.tri2, opts.tri3, opts.colors,
            opts.flip, name='slim', noLayer=True, **opts.attrs.pgon)

    stk.add(filled_polygon(opts.tri2, opts.colors.bg, **opts.attrs.pgon))

    stk.pop()


def _make_tiles(stk, tiles, n, noFlips, path, opts):
    if n == 0:
        return

    for ii,tri in enumerate(adjacent_tiles(opts.tri1, opts.side)):
        opts_ = opts.copy()
        path_ = path+str(ii)

        if not noFlips:
            opts_.flip = not opts_.flip

        a,b,c = tri
        d,e,f, g,h,i = inner(a,b,c, opts_.flip)

        opts_.points.update(zip(
            ('A','B','C', 'D','E','F', 'G','H','I'),
            ( a,  b,  c,   d,  e,  f,   g,  h,  i) ) )

        if tri not in tiles:
            tiles.add(tri)
            make_tile(stk, path_, opts_)

        _make_tiles(stk, tiles, n-1, noFlips, path_, opts_)


def make_tiles(n, noFlips=False, flipZero=False, opts=None):
    if opts is None:
        opts = defaults.copy()

    if flipZero:
        opts.flip = not opts.flip
        redraw(opts)

    stk = SVGStack()

    make_tile(stk, '0', opts)

    tiles = TileSet(opts.tri1)

    _make_tiles(stk, tiles, n, noFlips, '0', opts)

    stk[0].update(viewBox='{:f} {:f} {:f} {:f}'.format(*tiles.geo))

    return stk


class NonNegative(int):
    def __new__(cls, valueIn):
        valueOut = int(valueIn)

        if valueOut<0:
            raise ValueError('Non-negative integers only.')

        return int.__new__(cls, valueOut)


if __name__ == '__main__':
    from argparse import ArgumentParser

    psr = ArgumentParser()
    psr.add_argument( 'depth',    type=NonNegative)
    psr.add_argument('-noFlips',  action='store_true')
    psr.add_argument('-flipZero', action='store_true')

    args = psr.parse_args()

    print(make_tiles(args.depth, args.noFlips, args.flipZero))
