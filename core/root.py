
from __future__ import absolute_import

from .base import Element, tagAndRegister

from .misc import Layer, Title

from .util import attrs_to_xml

@tagAndRegister('svg')
class SVG(Element):
    def __init__(self, title, **attrs):
        self._stack      = None
        self._standAlone = None

        Element.__init__(self, version='1.1',
            xmlns='http://www.w3.org/2000/svg', **attrs)

        self['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'

        self.add(Title(title))

        self.inkscape_on()

    def standalone_no(self):
        self._standAlone = False

    def standalone_yes(self):
        self._standAlone = True

    def standalone_unset(self):
        self._standAlone = None

    def _copy_init(self, src):
        self._standAlone = src._standAlone
        Element._copy_init(self, src)

    def set_stack(self, stack):
        self._stack = stack

    def clear_stack(self):
        self._stack = None

    def __str__(self):
        return '<?xml version="1.0" encoding="utf-8"{}?>\n{}'.format(
            '' if self._standAlone is None else ' standalone="{}"'.format(
                'yes' if  self._standAlone else 'no'), Element.__str__(self) )

    @property
    def inky(self):
        return 'xmlns:inkscape' in self

    def inkscape_on(self):
        self['xmlns:inkscape'] = 'http://www.inkscape.org/namespaces/inkscape'

        for e in self:
            if isinstance(e, Layer):
                e._restore()

    def inkscape_off(self, removeLayers=False):
        """Removes xmlns:inkscape attribute; if removed, layers are replaced
        by their children, such that the children become siblings of the
        layer's siblings; if not removed, they are (reversably) demoted
        to ordinary groups."""

        if self.inked:
            removals = []

            for i,e in enumerate(self):
                if isinstance(e, Layer):
                    if removeLayers:
                        removals.append((i,e))
                    else:
                        e._demote()

            for i,e in reversed(removals):
                self._childred[i:i+1] = e._children

            del self['xmlns:inkscape']


    def remove(self, e):
        if isinstance(e, Layer):
            if e in self._stack:
                raise ValueError('Layer is active.')

        Element.remove(self, e)

    def _get_invisible_layers(self):
        return reversed(filter(
            lambda e: isinstance(e, Layer) and not e.visible, self))

    def purge_invisible_layers(self):
        for e in self._get_invisible_layers():
            self.remove(e)
