
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from  simplesvg import SVGStack
from     triphi import *

def make_tile(stk, opts):
    layerReg['slim'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['squat'](stk,
        opts.tri1, opts.tri2, opts.tri3,
        opts.colors, opts.flip, **opts.attrs.pgon)

    layerReg['ctrbg'](stk, opts.tri2, colors.bg, **opts.attrs.pgon)

def make_tiles(n, opts=None):
    if opts is None:
        opts = defaults.copy()

    stk = SVGStack()

    return stk

if __name__ == '__main__':
    import sys

    print(make_tiles(int(sys.argv[1])))
"""
This might be another instance where having a coefficient type might be
desired, not just an ABC (exponentiation by zero). Not sure that it's
worth the trouble, though. It would clash with the ABC, and probably
displace it, but then the test is less general. Maybe keep the ABC and
make the type None by default, which would replicate the current behavior.

The PEP3102 stuff in constructor might be avoided if the coefficients
had to be a single argument, rather than accepting them as individual
arguments. This is the way the standard library and built-ins work; I
can't think of any exceptions at the moment. Keyword-wise, sure. dict()
and dict.update() work this way, and it can lead to ambiguities :)

hmm, new in 3.3, ChainMap takes an arbitrary number of mappings, rather than an iterable of


The class factory would benefit from enforcing that the default arguments
must be keyword. A try/except SyntaxError with a docstring assignment later would work!

this is more about uniformly calling a variable bunch of subunits than specific to testing
  testing/validation and timing would be the obvious applications, though.
instantiate Multiplexer class in __init__
import instance from tests
use instance.register(name) as a decorator to register test functions
maybe other methods as decorators for setup/cleanup

sympy could substitute for polynomial
okay, what is really used is linear transform, matplotlib has something too
composition also, but functional is a dependency with or without polynomial
"""
