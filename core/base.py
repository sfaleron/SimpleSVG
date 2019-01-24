
from __future__ import absolute_import

from .root import Element, StackError

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

    def remove_child(self, e):
        if isinstance(e, Layer):
            if self._stack and self._stack[-1] is e:
                raise StackError('Layer is active.')

        Element.remove_child(self, e)

    def _get_invisible_layers(self):
        return reversed(filter(
            lambda x: isinstance(x, Layer) and not x.visible, self._children))

    def purge_invisible_layers(self):
        for e in self._get_invisible_layers():
            self.remove_child(e)
