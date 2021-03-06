
# A couple of standard library ideas.. ABC Mapping for Element?
# A number of applications for six module

from  __future__ import absolute_import

from .util import attrs_to_xml, SixDict3 as dict

try:
    basestring
except NameError:
    basestring = str


class Element(dict):
    """Iteration is over children, not keys."""

    def __init__(self, tag, **attrs):
        self._tag = tag
        self._root = None
        self._parent = None

        self._children  = []
        self._delimiter = '\n'

        dict.__init__(self, **attrs)

    @property
    def version(self):
        return self.root._ver if self.root else ''

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, e):
        self.set_root(e)

    def set_root(self, e):
        self._root = e
        for child in self:
            if isinstance(child, Element):
                child.root = e

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, e):
        self.set_parent(e)

    def set_parent(self, e):
        """An element may only have one parent and one root.
        It is up to the caller to remove the element from
        the previous (if any) parent's child list."""

        self._parent = e

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, x):
        self._delimiter = x

    # Called after attributes and child nodes are copied.
    def _copy_init(self, src):
        pass

    # theoretically, Elements with matching attributes could test
    # as equal, which should be avoided when managing children.
    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not (self is other)

    @property
    def tag(self):
        return type(self)._tag

    def __iter__(self):
        return iter(self._children)

    def add(self, e):
        self._children.append(e)

        if isinstance(e, Element):
            e.parent = self

        return e

    def add_many(self, *es):
        for e in es:
            self.add(e)

        return es

    def remove(self, e):
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
        cls = type(self)

        # doesn't call __init__()
        dupe = cls.__new__(cls)

        dupe.clear()
        dupe.update(self)
        dupe.update(kw)

        for e in self:
            dupe.add(e.copy())

        dupe._copy_init(self)

        return dupe

    def __str__(self):
        parts = ['<', self._tag, attrs_to_xml(self)]

        if self._children:
            parts += ['>', self._delimiter]

            for e in self:
                parts += [str(e), self._delimiter]

            parts += ['</', self._tag, '>']
        else:
            parts.append(' />')

        return ''.join(parts)


# Style element is implemented by the CSS class
class Style(dict):
    """What it says on the tin. A dictionary representation of the style attribute.
    Not to be confused with the Style element!"""

    @classmethod
    def parse(cls, styleAttr):
        return cls([(j.strip(), k.strip()) for j,k in [
            i.split(':') for i in styleAttr.split(';') if i]])

    def copy(self):
        return Style(**self)

    def __str__(self):
        return ';'.join(['%s:%s' % i for i in self.items()])


class StyledElement(Element):
    def __init__(self, tag, **attrs):
        Element.__init__(self, tag, **attrs)
        self._acquire_styles()

    def _acquire_styles(self):
        if 'style' in self:
            if isinstance(self['style'], Style):
                self['style'] = self['style'].copy()
            else:
                self['style'] = Style.parse(self['style'])
        else:
            self['style'] = Style()

    # Called after attributes and child nodes are copied.
    def _copy_init(self, src):
        Element._copy_init(self, src)
        self._acquire_styles()
