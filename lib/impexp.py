
from  __future__ import absolute_import

from ..core.base import Element, registry


import xml.etree.ElementTree as _ET

export = lambda root: _ET.ElementTree(_ET.fromstring(str(root)))

def _import_class(tag, attrs):
    flags = []

    if 'style' in self:
        flags.append('styled')
        self['style'] = Style.parse(self['style'])

    return registry.add(tag, *flags)(type(
        'Import'+tag.replace('-', '_'), (Element,), {}))


# will match run-on attributes, with no whitespace between the quoted
# value and the next attribute name. I don't think this is valid xml,
# but I'm not sure, and it's easy to accomodate.
#
# other sorts of invalid xml are likely to fail ungracefully, or even
# silently, simply dropping some or all attributes.

import re


attrib_r = re.compile(r'([^"\s]+)\s*=\s*"(.*?)"')

class Embed(Element):
    _tag = 'svg'
    _flags = ()

    def __init__(self, rawSVG):
        while True:
            starti  =  rawSVG.find('>')
            endi    = rawSVG.rfind('<')

            body    = rawSVG[starti+1:endi]

            starti  =  rawSVG.find('<')
            endi    =  rawSVG.find('>')

            if rawSVG[starti:].startswith('<?xml'):
                rawSVG = rawSVG[endi+1:]
            else:
                break

        attribs = {}

        for i in range(starti, endi):
            if rawSVG[i].isspace():
                attribs.update(attrib_r.findall(rawSVG[i:endi]))
                break

        Element.__init__(self, **attribs)

        self.add(body)

__all__ = ['export', 'Embed']
