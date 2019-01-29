
"""SimpleSVG
An increasing-more-complicated module for creating Inkscape-aware
SVG documents. No support is provided for loading/parsing documents,
and only a subset of the standard is supported. No dependencies, not
even the Standard Libary! EDIT: Oh drat. Almost."""

from __future__ import absolute_import

from .core.base    import Element, Style, registry
from .core.stack   import SVGStack, EmbedStack
from .core.root    import SVG
from .core.misc    import *
from .core.graphic import *

from . import lib
