
from __future__ import absolute_import

import xml.etree.ElementTree as _ET

from        .rtangles import *

try:
    from .decorations import *
except ImportError:
    pass

export = lambda root: _ET.ElementTree(_ET.fromstring(str(root)))
