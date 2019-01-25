
from __future__ import absolute_import

from    .rtangles import *
from .decorations import ArcDecorations, TickDecorations

import xml.etree.ElementTree as _ET

toET = lambda root: _ET.fromstring(str(root))
