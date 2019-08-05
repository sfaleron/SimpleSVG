
from __future__ import absolute_import

from .base import Element, StyledElement
from .util import unexpression_adder


__all__, adder = unexpression_adder()

@adder
class Group(StyledElement):
    def __init__(self, id_, **attrs):
        StyledElement.__init__(self, 'g', **attrs)
        self['id'] = id_

@adder
class Layer(Group):
    def __init__(self, id_, label, visible=False, **attrs):
        Group.__init__(self, id_, **attrs)
        self['inkscape:groupmode'] = 'layer'
        self['inkscape:label'] = label

        self.visible  = visible

        self.inkState = {}

    def _copy_init(self, src):
        self._inkState = src._inkState
        Group._copy_init(self, src)

    def _demote(self):
        for i in ('inkscape:groupmode', 'inkscape:label', 'style'):
            self._inkState[i] = self.pop(i)

    def _restore(self):
        self.update(self._inkState)

    @property
    def label(self):
        return self['inkscape:label']

    def visible_get(self):
        return self['style']['display'] == 'inline'

    def visible_set(self, state):
        self['style']['display'] = 'inline' if state else 'none'

    visible = property(visible_get, visible_set)


@adder
class ClipPath(StyledElement):
    def __init__(self, id_, **attrs):
        StyledElement.__init__(self, 'clipPath', **attrs)
        self['id'] = id_

@adder
class Use(Element):
    def __init__(self, ref, **attrs):
        Element.__init__(self, 'use', **attrs)
        self._href = '#'+ref

    def set_root(self, e):
        Element.set_root(self, e)

        self[('xlink:' if self.version[0] == '1' else '') + 'href'] = self._href

@adder
class Defs(Element):
    def __init__(self, **attrs):
        Element.__init__(self, 'defs', **attrs)

@adder
class Title(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, 'title', **attrs)
        self.add(body)

@adder
class Desc(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, 'desc', **attrs)
        self.add(body)

@adder
class TSpan(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, 'tspan', **attrs)
        self.delimiter = ''
        self.add(body)

@adder
class CData(str):
    def __new__(cls, cdata):
        return str.__new__(cls, '<![CDATA[{}]]>'.format(cdata))

@adder
# I've seen this wrapped in a defs element often, especially on W3C pages.
# Not super clear why that might be a good idea, or if it's considered a
# Best Practice. Easy enough for the calling code to wrap, if desired.
class CSS(Element):
    def __init__(self, **selectors):
        Element.__init__(self, 'style', **{'type':'text/css'})

        self.add(CData(''.join(['\n{} {{\n{}\n}}\n'.format(k,
            '\n'.join(['{}: {};'.format(*i) for i in v.items()]) )
                for k,v in selectors.items() ]) ))
