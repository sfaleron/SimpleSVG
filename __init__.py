
"""SimpleSVG
An increasing-more-complicated module for creating Inkscape-aware
SVG documents. No support is provided for loading/parsing documents,
and only a subset of the standard is supported. No dependencies, not
even the Standard Libary! EDIT: Oh drat. Almost."""

from __future__ import absolute_import

from .core.root   import Element, Style, StyledElement
from .core.misc   import Group, Layer, Defs, Clip, Use
from .core.stack  import SVGStack, EmbedStack
from .core.base   import SVG
from .core.styled import *

from . import lib
