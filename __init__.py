
"""SimpleSVG
An increasing-more-complicated module for creating Inkscape-aware
SVG documents. No support is provided for loading/parsing documents,
and only a subset of the standard is supported, although arbitrary
uninterpreted elements may be inserted verbatim."""

from __future__ import absolute_import

from .core.base    import Element, StyledElement, Style
from .core.stack   import SVGStack, EmbedStack
from .core.root    import SVG
from .core.misc    import *
from .core.graphic import *

from . import lib
