
from __future__ import absolute_import

from .root import Element, StackError

from .misc import Layer, Title

from .util import attrs_to_xml

class SVG(Element):
    def __init__(self, title, **attrs):
        self._stack  = None
        self._xAttrs = attrs.pop('xmlattrs', {})

        Element.__init__(self, 'svg', version='1.1',
            xmlns='http://www.w3.org/2000/svg', **attrs)

        self['xmlns:xlink']    = 'http://www.w3.org/1999/xlink'
        self['xmlns:inkscape'] = 'http://www.inkscape.org/namespaces/inkscape'

        self.add_child(Title(title))

    def set_stack(self, stack):
        self._stack = stack

    def clear_stack(self):
        self._stack = None

    def __str__(self):
        return '<?xml version="1.0" encoding="utf-8" {}?>\n{}'.format(
            attrs_to_xml(self._xAttrs), Element.__str__(self) )

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
