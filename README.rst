
**SimpleSVG** creates `Inkscape`_-aware SVG documents with support for layers and groups. It is equally at home under Python2 or Python3.

No dependencies in the core components; some of the classes and functions under
``lib/`` use the Standard Library. I'm not sure that generating SVG is a typical application in a stripped-down environment, but here it is!

Arguments destined to be attribute values are converted to strings and left uninterpreted as much as possible. The notable exception made is for booleans. ``str(True)`` and ``str(False)`` don't do the useful thing. For that matter, ``bool('False')`` doesn't either. When passing booleans explicitly as strings, use what SVG expects, ``'0'`` or ``'1'``.

Uninterpreted, passed-through keyword arguments are handled similarly. If a subclass of bool should't be converted to an int before becoming a string, wrap it and delegate
``__str__()`` or ``__format__()`` (or define these explicitly, if control over the
source is available). If a suitable predicate is available, use of customized
serialization is recommended, via ``add_attrSerializer()``. The boolean handling is
implemented in this manner, in ``core/util.py``, with explanations. Use it as a template and documentation.

Note that the conversion is only made when the element is serialized, and this occurs on-demand in a synchronous manner, without any retention, so any side-effects occurring within nontrivial objects stored as attributes will remain as long as the object is among an element's attributes. The ``freeze_attrs()`` method will permanently stringify an iterable of attribute names, or all of them, if no iterable is provided.

Most core classes are straightforward wrappers, and offer small enhancements over building XML from one of the usual suspects. SVGStack and the other small enhancements may be enough collectively to make this library useful, but where it really shines is the Path class and the library classes that build upon it. Check 'em out!

Export to `ElementTree`_ is supported.

Only a dozen or so element types are explicitly supported, but arbitary XML is supported via the make_element() factory.

Aims to comply with SVG v1.1, with some v2.0 support. How much compliance to which standard is mostly up to the user of the library, though.

`SVGwrite`_ is a nice-looking alternate. It depends on `pyparser`_, a fabulous and well-maintained package. All pure-python. I expect I passed it over to keep things "simple". Software has a troublesome way of not staying simple :)

Suggestions for further exploration of SVG:

- https://developer.mozilla.org/en-US/docs/Web/SVG
- https://www.w3.org/Graphics/SVG/
- https://jwatt.org/svg/authoring/
- https://flaviocopes.com/svg/

API Documentation is lacking, but the ``samples/`` should help, as should the main motivation for writing this, the `TriPhi`_ application, which generates my avatar and explores the `mathematical structure`_ within.

----

This package is functional for some cases some of the time, but is far from 1.0 status. Do not rely on a stable API, or a stable anything else, for that matter!


.. _Inkscape: https://inkscape.org/
.. _TriPhi: https://github.com/sfaleron/TriPhi
.. _mathematical structure: https://www.mathcha.io/editor/vEBYC1KFnvu2vIy2

.. _svgwrite: https://pypi.org/project/svgwrite/
.. _pyparser: https://pypi.org/project/pyparsing/

.. _ElementTree: https://docs.python.org/library/xml.etree.elementtree.html
