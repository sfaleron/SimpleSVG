
from __future__ import division
from __future__ import absolute_import

import  os.path     as osp
from       math import sin, cos

from  simplesvg import Polygon, Text, Line, StyledElement, filled_polygon
from   .keyattr import KeywordToAttr, kw2aDec, AttribItem
from   .options import standardSide

from   registry import RegistryMap


def rotate_left(seq):
    return seq[ 1:] + seq[: 1]

def rotate_right(seq):
    return seq[-1:] + seq[:-1]

layerReg = RegistryMap(passName=True)

@kw2aDec
class LayerInfo(KeywordToAttr):
    _attribs = map(AttribItem, ['layer', 'path'])


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
    name    = kw.pop('name')
    noLayer = kw.pop('noLayer', False)

    clr  = getattr(colors, name)

    notShared = dict(slim=rotate_left(tri2), squat=rotate_right(tri2))[
        dict(slim='squat', squat='slim')[name] if flip else name]

    pts1, pts2, pts3 = zip(tri1, tri3, notShared)


    if not noLayer:
        info = LayerInfo(
            layer = stk.push_layer(name, True),
            path  = stk.push_group(name) )
    else:
        # for tiling
        info = None

    stk.add(filled_polygon(pts1, clr, **kw))
    stk.add(filled_polygon(pts2, clr, **kw))
    stk.add(filled_polygon(pts3, clr, **kw))

    if not noLayer:
        stk.pop(); stk.pop()

    return info

layerReg('background', disabledLayer(boundary(filled_polygon_layer)))

layerReg( 'slim', mixed_up_triangles)
layerReg('squat', mixed_up_triangles)

layerReg('ctrsl', disabledLayer(filled_polygon_layer))
layerReg('ctrsq', disabledLayer(filled_polygon_layer))
layerReg('ctrbg', layer(filled_polygon_layer))

@layerReg('rays')
def rays(stk, pts1, pts2, flip, name, **kw):
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
        pts2 = rotate_left(pts2)
    else:
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
