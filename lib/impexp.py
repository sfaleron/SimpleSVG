
from  __future__ import absolute_import

from ..core.base import Element, registry


import xml.etree.ElementTree as _ET

export = lambda root: _ET.fromstring(str(root))

def _import_class(tag, attrs):
    flags = []

    if 'style' in self:
        flags.append('styled')
        self['style'] = Style.parse(self['style'])

    return registry.add(tag, *flags)(type(
        'Import'+tag.replace('-', '_'), (Element,), {}))
