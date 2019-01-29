
# A couple of standard library ideas.. ABC Mapping for Element?
# A number of applications for six module

from  __future__ import absolute_import

from .util import attrs_to_xml

try:
    basestring
except NameError:
    basestring = str


class Registry(object):
    def __init__(self):
        self._store = {}
        self._flags = set(['styled'])

    @property
    def flags(self):
        return self._flags

    def add(self, tag, *flags):
        for flag in flags:
            if not flag in self._flags:
                raise ValueError("Flag '{}' not recognized.".format(flag))

        def dec(x):
            self._store[tag] = x

            x._flags = flags
            x._tag   = tag
            return x

        return dec

    def __contains__(self, tag):
        return tag in self._store

    def deregister(self, tag):
        if tag in self:
            return self._store.pop(tag)
        else:
            raise ValueError('Tag "{}" not found.'.format(tag))

registry = Registry()


class Element(dict):
    """Iteration is over children, not keys."""

    def __init__(self, **attrs):
        self._children = []
        self.update(attrs)

        if 'styled' in self.flags:
            if 'style' in self:
                if isinstance(self['style'], Style):
                    self['style'] = self['style'].copy()
                else:
                    self['style'] = Style.parse(self['style'])
            else:
                self['style'] = Style()

    # Called after attributes and child nodes are copied.
    def _copy_init(self, src):
        if 'styled' in self.flags:
            if 'style' in self:
                if isinstance(self['style'], Style):
                    self['style'] = self['style'].copy()
                else:
                    self['style'] = Style.parse(self['style'])

    # Called after xml attributes and child nodes are imported.
    # src is presumed to be an ElementTree element.
    #
    # ** This should be done by the importer with a new class **
    def _import_init(self, src):
        self._tag = src.tag

        flags = []

        if 'style' in self:
            flags.append('styled')
            self['style'] = Style.parse(self['style'])

        self._flags = tuple(flags)

    # theoretically, Elements with matching attributes could test
    # as equal, which should be avoided when managing children.
    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not (self is other)

    @property
    def tag(self):
        return type(self)._tag

    @property
    def flags(self):
        return type(self)._flags

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
        return '<%s%s%s\n' % (self._tag, attrs_to_xml(self),
            '>\n%s</%s>' % (''.join(['{}\n'.format(i) for i in self]),
                self._tag) if self._children else ' />')

    if hasattr(dict, 'iteritems'):
        items = dict.iteritems


class Style(dict):
    """What it says on the tin. A dictionary representation of the style attribute.
    Not to be confused with the Style element!"""

    @classmethod
    def parse(styleAttr):
        return Style([(j.strip(), k.strip()) for j,k in [
            i.split(':') for i in styleAttr.split(';') if i]])

    def __str__(self):
        return ';'.join(['%s:%s' % i for i in self.items()])

    if hasattr(dict, 'iteritems'):
        items = dict.iteritems
