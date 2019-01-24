
from __future__ import absolute_import

from .root import Element, StackError

from .base import SVG

from .misc import Layer, Group, Clip, Defs


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

        self._layers = 0

    @property
    def layers(self):
        return tuple(self._layers)

    def push_layer(self, label, visible=False):
        if len(self) != 1:
            raise StackError('Layers may only descend from the root.')

        self._layers += 1

        return self._push(Layer('layer{:d}'.format(self._layers), label, visible))


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
