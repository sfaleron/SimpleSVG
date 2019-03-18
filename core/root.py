
from __future__ import absolute_import

from .base import Element, registry

from .misc import Layer, Title

allFlags = {'inkOffsetFix'}

@registry.add('svg', 'styled')
class SVG(Element):
    # version should be passed as a string
    def __init__(self, title, version='1.1', docFlags=frozenset(), **attrs):
        self._stack       = None
        self._standAlone  = None

        self._docFlags    = set()
        self._styleSheets = set()

        for flag in docFlags:
            self.docFlag_set(flag)

        tmp = version.split('.')

        major = tmp[0]
        minor = tmp[1] if len(tmp)>1 else '0'

        self._ver = (major, minor)

        Element.__init__(self, xmlns='http://www.w3.org/2000/svg', **attrs)

        if major == '1':
            self[  'version'  ] = version
            self['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'

        self.add(Title(title))

        self.inkscape_on()

    def add(self, e):
        Element.add(self, e)

        if isinstance(e, Element):
            e.root = self

        return e

    def standalone_no(self):
        self._standAlone = False

    def standalone_yes(self):
        self._standAlone = True

    def standalone_unset(self):
        self._standAlone = None

    def docFlag_set(self, flag):
        if flag in allFlags:
            self._docFlags.add(flag)
        else:
            raise ValueError("Flag '{}' not recognized.".format(flag))

    def docFlag_clear(self, flag):
        if flag in allFlags:
            self._docFlags.discard(flag)
        else:
            raise ValueError("Flag '{}' not recognized.".format(flag))

    @property
    def docFlags(self):
        return self._docFlags

    @property
    def styleSheets(self):
        return self._styleSheets

    def _copy_init(self, src):
        self._standAlone = src._standAlone
        Element._copy_init(self, src)

    def set_stack(self, stack):
        self._stack = stack

    def clear_stack(self):
        self._stack = None

    def __str__(self):
        return '<?xml version="1.0" encoding="utf-8" {2}?>\n{0}{1}'.format(
            ''.join(['<?xml-stylesheet href="{}" type="text/css" ?>\n'.format(
                sheet) for sheet in self._styleSheets]), Element.__str__(self),
            {True: 'standalone="yes" ', False: 'standalone="no" ',
                None: ''}[self._standAlone] )

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
