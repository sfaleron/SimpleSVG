
from __future__ import absolute_import

from .base import Element, Style, registry
from .util import unexpression_adder


__all__, adder = unexpression_adder()

@adder
@registry.add('g', 'styled')
class Group(Element):
    def __init__(self, id_, **attrs):
        Element.__init__(self, **attrs)
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
        Element._copy_init(self, src)

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
@registry.add('clipPath', 'styled')
class ClipPath(Element):
    def __init__(self, id_, **attrs):
        Element.__init__(self, **attrs)
        self['id'] = id_

@adder
@registry.add('use')
class Use(Element):
    def __init__(self, ref, **attrs):
        Element.__init__(self, **attrs)
        self._href = '#'+ref

    def set_root(self, e):
        Element.set_root(self, e)

        self[('xlink:' if self.version[0] == '1' else '') + 'href'] = self._href

@adder
@registry.add('defs')
class Defs(Element):
    pass

@adder
@registry.add('title')
class Title(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, **attrs)
        self.add(body)

@adder
@registry.add('desc')
class Desc(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, **attrs)
        self.add(body)

@adder
@registry.add('tspan')
class TSpan(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, **attrs)
        self.delimiter = ''
        self.add(body)
