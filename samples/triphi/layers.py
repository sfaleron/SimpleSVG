
from __future__ import division
from __future__ import absolute_import

import  os.path     as osp
from       math import sin, cos

from  simplesvg import Polygon, Text, Line, StyledElement, filled_polygon
from   .keyattr import KeywordToAttr
from   .options import standardSide

from   registry import RegistryMap


def rotate_left(seq):
    return seq[ 1:] + seq[: 1]

def rotate_right(seq):
    return seq[-1:] + seq[:-1]

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

def mixed_up_triangles(stk, tri1, tri2, tri3, colors, flip, **kw):
    name = kw.pop('name')
    clr  = getattr(colors, name)

    tri3 = rotate_left(tri3)

    tri2 = dict(
        squat = {True:rotate_left, False:rotate_right},
        slim  = {True:rotate_right, False:rotate_left} )[name][flip](tri2)

    pts1, pts2, pts3 = tuple(zip(tri1, tri2, tri3))

    info = LayerInfo(
        layer = stk.push_layer(name, True),
        path  = stk.push_group(name) )

    filled_polygon_layer(stk, pts1, clr, **kw)
    filled_polygon_layer(stk, pts2, clr, **kw)
    filled_polygon_layer(stk, pts3, clr, **kw)

    stk.pop(); stk.pop()

    return info

layerReg('background', disabledLayer(boundary(filled_polygon_layer)))

layerReg( 'slim', mixed_up_triangles)
layerReg('squat', mixed_up_triangles)

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
        pts2 = rotate_right(pts2)

    for p1, p2 in zip(pts1, pts2):
        stk.add(Line(p1, p2, **kw))

    stk.pop(); stk.pop()

    return info


import xml.etree.ElementTree as ET

@layerReg('glyph')
@layer
def _(stk, side, center):
    attribs = ET.parse(osp.join(osp.dirname(
        __file__), 'phiglyph.svg')).getroot().attrib

    attribs.update(transform='translate({:f} {:f}) scale({:f})'.format(
        center.x, center.y, side/standardSide))

    return LayerInfo(
        path = stk.add(StyledElement('path', **attribs)) )

@layerReg('labels')
@disabledLayer
def _(stk, lbls, pts, size=None):

    info = LayerInfo(
        path = stk.push_group('labels') )


    for k, lbl, pt in [(kk, lbls[kk], pts[kk]) for kk in lbls]:

        if lbl.r is None:
            dx, dy = lbl.dx, lbl.dy
        else:
            dx, dy = lbl.r*size*cos(lbl.theta), -lbl.r*size*sin(lbl.theta)

        stk.add(Text((pt.x+dx, pt.y+dy), k))

    stk.pop()

    return info
