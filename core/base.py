
# A couple of standard library ideas.. ABC Mapping for Element?
# A number of applications for six module

from  __future__ import absolute_import

from .util import attrs_to_xml, PY2

try:
    basestring
except NameError:
    basestring = str

# For importing
_tagRegistry = {}

def tagAndRegister(name):
    def dec(x):
        _tagRegistry[name] = x
        x._tag = name
        return x

    return dec


class Element(dict):
    """Iteration is over children, not keys."""

    def __init__(self, **attrs):
        self._children = []
        self.update(attrs)

    # Called after attributes and child nodes are copied.
    def _copy_init(self, src):
        self._tag = src._tag

    # Called after xml attributes and child nodes are imported.
    # src is presumed to be an ElementTree element.
    def _import_init(self, src):
        self._tag = src.tag

    # theoretically, Elements with matching attributes could test
    # as equal, which should be avoided when managing children.
    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not (self is other)

    @property
    def tag(self):
        return self._tag

    def __iter__(self):
        return iter(self._children)

    def add(self, e):
        self._children.append(e)
        return e

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
    def __init__(self, **attrs):
        attrs['style'] = Style(**attrs.get('style', {}))
        Element.__init__(self, **attrs)
