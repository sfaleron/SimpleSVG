
"""SimpleSVG
An increasing-more-complicated module for creating Inkscape-aware
SVG documents. No support is provided for loading/parsing documents,
and only a subset of the standard is supported. No dependencies, not
even the Standard Libary! EDIT: Oh drat. Almost."""

# note that coordinate values may be numeric or stringy, or
# indeed, anything that has a __str__() member!

import sys

_PY2 = sys.version_info[0] < 3

del sys

try:
    from copy import deepcopy as _deepcopy
except ImportError:
    _deepcopy = None

class StackError(Exception):
    pass

def _copy(o):
    if callable(_deepcopy):
        return _deepcopy(o)
    else:
        raise NotImplementedError('unable to comply')


class Element(dict):
    def __init__(self, tag, **attrs):
        self._tag = tag
        self._children = []
        self.update(attrs)

    @property
    def tag(self):
        return self._tag

    def add_child(self, e):
        self._children.append(e)
        return e

    def remove_child(self, e):
        self._children.remove(e)

    def copy(self):
        return _copy(self)

    def __str__(self):
        return '<%s %s%s\n' % (self._tag, ' '.join(['%s="%s"' % i for i in self.items()]),
            '>\n%s\n</%s>' % ('\n'.join(map(str, self._children)), self._tag) if self._children else ' />')

    if _PY2:
        @property
        def items(self):
            return self.iteritems

class Style(dict):
    """What it says on the tin. A dictionary representation of the style attribute.
    Not to be confused with the Style element!"""
    def __str__(self):
        return ';'.join(['%s:%s' % i for i in self.items()])

    if _PY2:
        @property
        def items(self):
            return self.iteritems

class StyledElement(Element):
    def __init__(self, tag, **attrs):
        attrs['style'] = Style(**attrs.get('style', {}))
        Element.__init__(self, tag, **attrs)

class Group(Element):
    def __init__(self, id_, **attrs):
        Element.__init__(self, 'g', **attrs)
        self['id'] = id_

    def copy(self, newid=None):
        newgrp = Element.copy(self)
        if newid:
            newgrp['id'] = newid

        return newgrp

class Layer(Group):
    def __init__(self, id_, label, visible=False, **attrs):
        Group.__init__(self, id_, **attrs)
        self['inkscape:groupmode'] = 'layer'
        self['inkscape:label'] = label
        self['style'] = Style()

        self.visible = visible

    def copy(self, newid=None, newlbl=None):
        newlyr = Group.copy(self, newid)
        if newlbl:
            newlyr['inkscape:label'] = newid

        return newlyr

    def visible_get(self):
        return self['style']['display'] == 'inline'

    def visible_set(self, state):
        self['style']['display'] = 'inline' if state else 'none'

    visible = property(visible_get, visible_set)

    @property
    def label(self):
        return self['inkscape:label']

    def __hash__(self):
        return hash(self.label)

class SVG(Element):
    def __init__(self, **attrs):
        self._stack = None

        Element.__init__(self, 'svg', xmlns='http://www.w3.org/2000/svg', version='1.1', baseProfile='tiny', **attrs)
        self['xmlns:inkscape'] = 'http://www.inkscape.org/namespaces/inkscape'

    def set_stack(self, stack):
        self._stack = stack

    def clear_stack(self):
        self._stack = None

    def __str__(self):
        return '<?xml version="1.0" encoding="utf-8"?>\n' + Element.__str__(self)

    def remove_child(self, e):
        if self._stack and isinstance(e, Layer):
            self._stack.remove_layer(e)

        Element.remove_child(self, e)


    def _get_invisible_layers(self):
        return reversed(filter(
            lambda x: isinstance(x, Layer) and not x.visible, self._children))

    def purge_invisible_layers(self):
        for e in self._get_invisible_layers():
            self.remove_child(e)


class _Stack(list):
    def copy(self):
        return _copy(self)

    def _push(self, item):
        self.append(self[-1].add_child(item))
        return item

    def pop(self):
        return list.pop(self)

    def add(self, item):
        return self[-1].add_child(item)

    def push_group(self, id_):
        return self._push(Group(id_))

    def push_clip(self, id_):
        return self._push(Clip(id_))

    def push_defs(self):
        return self._push(Defs())

    def __str__(self):
        return str(self[0])

class SVGStack(_Stack):
    def __init__(self, appendTo=None, **kw):
        if appendTo and not isinstance(appendTo, SVG):
            raise StackError('SVGStack may only be associated to the root of a document.')

        _Stack.__init__(self, [appendTo if appendTo else SVG(**kw)])

        self[0].set_stack(self)

        self._layers = []
        self._n = 0

    @property
    def layers(self):
        return tuple(self._layers)

    def push_layer(self, label, visible=False):
        if len(self) != 1:
            raise StackError('Layers may only descend from the root.')

        self._n += 1

        e = self._push(Layer('layer'+str(self._n), label, visible))
        self._layers.append(e)
        return e

    def remove_layer(self, e):
        if e in self._layers:
            if e in self:
                raise StackError('Layer is active.')

            self._layers.remove(e)

    def purge_invisible_layers(self):
        if len(self) != 1:
            raise StackError('Return to root before modifying layers.')

        self[0].purge_invisible_layers()

class _EmbeddedCont(Element):
    def __init__(self):
        Element.__init__(self, 'embed/null')

    def __str__(self):
        return '\n'.join(map(str, self._children))

class EmbedStack(_Stack):
    def __init__(self, *args):
        args += ([_EmbeddedCont()],)
        _Stack.__init__(self, *args)

    def embed(self, parent):
        for e in self:
            parent.add_child(e)

# only relative movements!
class Path(StyledElement):
    def __init__(self, initial_pos, **attrs):
        StyledElement.__init__(self, 'path', **attrs)
        self.steps = ['M%s,%s' % tuple(initial_pos)]

    def lineTo(self, pt):
        self.steps.append('l%s %s' % tuple(pt))

    def lineToMany(self, many):
        self.steps.append('l' + 'l'.join(['%s %s' % tuple(i) for i in many]))

    def arcTo(self, pt, rx, ry, rot, bigArc=False, incAngle=True):
        """https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes"""
        self.steps.append('a%s,%s %s %s,%s %s,%s' %
            (rx, ry, rot, int(bool(bigArc)), int(bool(incAngle)), pt[0], pt[1]))

    def close(self):
        return self.steps.append('z')

    def __str__(self):
        self['d'] = '\n'.join(self.steps)
        return StyledElement.__str__(self)

class Polygon(StyledElement):
    def __init__(self, pts, **attrs):
        StyledElement.__init__(self, 'polygon',
            points = ' '.join(['%s,%s' % tuple(i) for i in pts]), **attrs)

def filled_polygon(pts, fillColor, **attrs):
    return Polygon(pts, fill=fillColor, **attrs)

class Line(StyledElement):
    def __init__(self, pt1, pt2, **attrs):
        StyledElement.__init__(self, 'line',
            x1=pt1[0], y1=pt1[1], x2=pt2[0], y2=pt2[1], **attrs)

class Rect(StyledElement):
    def __init__(self, pt, w, h, rx='0', ry='0', **attrs):
        StyledElement.__init__(self, 'rect',
            x=pt[0], y=pt[1], width=w, height=h, rx=rx, ry=ry, **attrs)

class Circle(StyledElement):
    def __init__(self, ctr, r, **attrs):
        StyledElement.__init__(self, 'circle', cx=ctr[0], cy=ctr[1], r=r, **attrs)

class Text(StyledElement):
    def __init__(self, pt, text, **attrs):
        StyledElement.__init__(self, 'text', x=pt[0], y=pt[1], **attrs)
        self.add_child(text)


class Clip(Element):
    def __init__(self, id_, **attrs):
        Element.__init__(self, 'clipPath', **attrs)
        self['id'] = id_

class Use(Element):
    def __init__(self, ref, **attrs):
        Element.__init__(self, 'use', **attrs)
        self['xlink:href'] = '#'+ref

class Defs(Element):
    def __init__(self, **attrs):
        Element.__init__(self, 'defs', **attrs)
