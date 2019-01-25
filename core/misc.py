
from __future__ import absolute_import

from .base import Element, Style


class Group(Element):
    def __init__(self, id_, **attrs):
        Element.__init__(self, 'g', **attrs)
        self['id'] = id_

class Layer(Group):
    _copyAttributes = ('_inkState',)

    def __init__(self, id_, label, visible=False, **attrs):
        Group.__init__(self, id_, **attrs)
        self['inkscape:groupmode'] = 'layer'
        self['inkscape:label'] = label
        self['style'] = Style()

        self.visible  = visible

        self.inkState = {}

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

class Title(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, 'title', **attrs)
        self.add_child(body)

class Desc(Element):
    def __init__(self, body, **attrs):
        Element.__init__(self, 'desc', **attrs)
        self.add_child(body)
