
from __future__ import absolute_import

from .root import Element, Style


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
