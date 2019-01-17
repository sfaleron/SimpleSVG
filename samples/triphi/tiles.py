
# Keep track of tiles by converting coordinates to fixed point for storing and lookups
#

from  __future__ import absolute_import

from  itertools  import combinations

from .keyattr    import KeywordToAttr, kw2aDec, AttribItem
from .math       import inner, triangles_from_side


@kw2aDec
class Extents(KeywordToAttr):
    _attribs = map(AttribItem, ['xmin', 'xmax', 'ymin', 'ymax', 'empty'])


def fixedPt(n, prec=16):
    return int(round(n*2**prec, 0))

class Tile(frozenset):
    def __new__(cls, pts):
        return frozenset.__new__(cls,
            [(fixedPt(pt.x), fixedPt(pt.y)) for pt in pts])

# Also track extents as tiles are added

class TileSet(object):
    def __init__(self, pts=None):
        self._tileSet = set()
        self._extents = Extents(empty=True)

        if pts:
            self.add(pts)

    def __contains__(self, pts):
        return Tile(pts) in self._tileSet

    def add(self, pts):
        xs, ys = zip(*pts)

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        extents = self._extents

        if extents.empty:
            extents.update(empty=False,
                xmin=xmin, ymin=ymin,
                xmax=xmax, ymax=ymax )
        else:
            extents.update(
                xmin=min(xmin, extents.xmin),
                xmax=max(xmax, extents.xmax),
                ymin=min(ymin, extents.ymin),
                ymax=max(ymax, extents.ymax) )

        self._tileSet.add(Tile(pts))

    @property
    def geo(self):
        xts = self._extents
        return (xts.xmin, xts.ymin, (xts.xmax-xts.xmin), (xts.ymax-xts.ymin))

    @property
    def dims(self):
        return self.geo[2:]

def adjacent_tiles(triIn, side=None):
    for a,b in combinations(triIn, 2):
        triX,triY = triangles_from_side(a, b, side)

        # retain the triangle that isn't the "spawning" triangle
        yield triY if hash(Tile(triIn)) == hash(Tile(triX)) else triX
