
from __future__ import absolute_import

from .root import SVG

from .misc import Layer, Group, ClipPath, Defs

class StackError(Exception):
    pass


class _Stack(list):
    def __init__(self, baseNode):
        list.__init__(self, [baseNode])

    def _push(self, item):
        self.append(self[-1].add(item))
        return item

    def pop(self):
        return list.pop(self)

    def add(self, item):
        return self[-1].add(item)

    def push_group(self, id_, **attrs):
        return self._push(Group(id_, **attrs))

    def push_clippath(self, id_, **attrs):
        return self._push(ClipPath(id_, **attrs))

    def push_defs(self, **attrs):
        return self._push(Defs(**attrs))

    def __str__(self):
        return str(self[0])

    @property
    def baseNode(self):
        return self[0]

class SVGStack(_Stack):
    def __init__(self, baseNode):
        if not isinstance(baseNode, SVG):
            raise StackError('SVGStack may only be associated to the root of a document.')

        _Stack.__init__(self, baseNode)

        self[0].set_stack(self)

        self._layers = 0

    @property
    def layers(self):
        return tuple(self._layers)

    def push_layer(self, label, visible=False, **attrs):
        if len(self) != 1:
            raise StackError('Layers may only descend from the root.')

        self._layers += 1

        return self._push(Layer('layer{:d}'.format(self._layers), label, visible, **attrs))

class EmbedStack(_Stack):
    pass
