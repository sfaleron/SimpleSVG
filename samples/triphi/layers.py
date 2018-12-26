
from __future__ import absolute_import

import  os.path     as osp
from       math import sin, cos

from   registry import RegistryMap

from  simplesvg import Polygon, Text, Line, filled_polygon

from   .keyattr import KeywordToAttr



layerReg = RegistryMap(passName=True)

class LayerInfo(KeywordToAttr):
    __slots__ = ('layer', 'path')


def layer_decorator(visible):
    def dec(f):
        def g(stk, *args, **kw):
            name = kw.pop('name')

            g = stk.push_layer(name, visible)
            info = f(stk, *args, **kw)
            info.layer = g
            stk.pop()

            return info
        return g
    return dec

layer         = layer_decorator(True)
disabledLayer = layer_decorator(False)


def filled_polygon_layer(stk, *args, **kw):
    return LayerInfo(
        path = stk.add(filled_polygon(*args, **kw)) )

def boundary(f):
    def g(*args, **kw):
        info = f(*args, **kw)
        info.path['id'] = 'boundary'
        return info

    return g

layerReg('background', disabledLayer(boundary(filled_polygon_layer)))

layerReg('ctrsl', disabledLayer(filled_polygon_layer))

layerReg('ctrsq', disabledLayer(filled_polygon_layer))

layerReg('ctrbg', layer(filled_polygon_layer))

@layerReg('rays')
def _(stk, pts1, pts2, flip, name, **kw):
    if len(pts1) != len(pts2):
        raise ValueError('Point sequences much be of equal length.')

    stk.push_defs()
    stk.push_clip('trim'),
    stk.add(Polygon(pts1))

    stk.pop(); stk.pop()

    info = LayerInfo(
        layer = stk.push_layer(name, True),
        path  = stk.push_group(name) )

    info.path['clip-path'] = 'url(#trim)'

    if flip:
        # rotate right one element
        pts2 = pts2[-1:]+pts2[:-1]

    for p1, p2 in zip(pts1, pts2):
        stk.add(Line(p1, p2, **kw))

    stk.pop(); stk.pop()

    return info

@layerReg('glyph')
@layer
def _(stk):
    return LayerInfo(
        path  = stk.add(open(osp.join(osp.dirname(
            __file__), 'phiglyph.svg'), 'r').read()) )

@layerReg('labels')
@disabledLayer
def _(stk, lbls, pts, size=None):

    info = LayerInfo(
        path = stk.push_group('labels') )


    for k, lbl, pt in [(kk, lbls[kk], pts[kk]) for kk in lbls]:

        if lbl.r is None:
            dx, dy = lbl.dx, lbl.dy
        else:
            dx, dy = lbl.r*size*cos(lbl.theta), lbl.r*size*sin(lbl.theta)

        stk.add(Text((pt.x+dx, pt.y+dy), k))

    stk.pop()

    return info
