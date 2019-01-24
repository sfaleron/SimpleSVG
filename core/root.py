
from  __future__ import absolute_import

from .util import attrs_to_xml

PY2 = hasattr(dict, 'iteritems')

class StackError(Exception):
    pass


class Element(dict):
    def __init__(self, tag, **attrs):
        self._tag = tag
        self._children = []
        self.update(attrs)

    @property
    def tag(self):
        return self._tag

    def add_child(self, e):
        self._children.append(e)
        return e

    def remove_child(self, e):
        self._children.remove(e)

    def copy(self):
        """Recursive copy"""

        pass

    def __str__(self):
        return '<%s %s%s\n' % (self._tag, attrs_to_xml(self),
            '>\n%s\n</%s>' % ('\n'.join(map(str, self._children)),
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
