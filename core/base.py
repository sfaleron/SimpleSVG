
from __future__ import absolute_import

from .root import Element

from .misc import Layer


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

    # this probably should work for any child, certainly Group instances.
    # It also seems like it doesn't belong here, which may indicate some-
    # thing curious about the stack type, if it's just a recapitulation
    # of the root node's children. It is when the root is the top element..
    # so the stack should operate somehow on the top node's children?

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
