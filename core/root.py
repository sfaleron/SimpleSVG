
from  __future__ import absolute_import

from .util import attrs_to_xml, PY2

try:
    basestring
except NameError:
    basestring = str

class StackError(Exception):
    pass


class Element(dict):
    """Iteration is over children, not keys."""

    _copyAttributes = ()

    def __new__(cls, *args, **kw):
        o = dict.__new__(cls, *args, **kw)
        o._init_args = (args, kw)
        return o

    def __init__(self, tag, **attrs):
        self._tag = tag
        self._children = []
        self.update(attrs)

    @property
    def tag(self):
        return self._tag

    def __iter__(self):
        return iter(self._children)

    def add_child(self, e):
        self._children.append(e)
        return e

    def remove_child(self, e):
        self._children.remove(e)

    def freeze_attrs(self, it=None):
        if it is None:
            it = self.keys()

        for k in it:
            v = self[k]
            if not isinstance(v, basestring):
                self[k] = str(int(v) if isinstance(v, bool) else v)

    def copy(self, **kw):
        """Children are copied recursively, but attributes are a shallow-copy"""
        args, kw = self._init_args
        cls  = type(self)
        dupe = cls(*args, **kw)
        dupe.clear()
        dupe.update(self)
        dupe.update(kw)

        for name in cls._copyAttributes:
            setattr(dupe, name, getattr(self, name))

        while dupe._children:
            dupe.remove_child(dupe._children[0])

        for e in self:
            dupe.add_child(e.copy())

        return dupe


    def __str__(self):
        return '<%s %s%s\n' % (self._tag, attrs_to_xml(self),
            '>\n%s\n</%s>' % ('\n'.join(map(str, self)),
                self._tag) if self._children else ' />')

    if PY2:
        @property
        def items(self):
            return self.iteritems

class Style(dict):
    """What it says on the tin. A dictionary representation of the style attribute.
    Not to be confused with the Style element!"""

    def __str__(self):
        return ';'.join(['%s:%s' % i for i in self.items()])

    if PY2:
        @property
        def items(self):
            return self.iteritems

class StyledElement(Element):
    def __init__(self, tag, **attrs):
        attrs['style'] = Style(**attrs.get('style', {}))
        Element.__init__(self, tag, **attrs)
