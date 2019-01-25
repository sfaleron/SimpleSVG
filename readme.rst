
SimpleSVG creates Inkscape-aware SVG documents with support for layers and groups.

No dependencies; the core components don't even use the Standard Library. I'm not sure that generating SVG is a typical application in a stripped-down environment, but here it is!

Arguments dentined to be attribute values are converted to string and not interpreted as much as possible. The notable exception is booleans. str(True) and str(False) don't do the useful thing. For that matter, bool('False') wouldn't either. When passing explicit strings, use what SVG expects, '0' or '1'.

Uninterpreted, passed-through keyword arguments are handled similarly. If you have a subclass of bool that you don't want converted to an int before becoming a string, wrap it and delegate __str__() or __format__().

Note that the conversion is only made when the element is serialized, and the serialized form is not stored, so any interesting side-effects occuring within nontrivial objects stored as attributes will be in effect as long as the object is among an element's attributes. The freeze_attrs() method will permanently stringify an interable of attribute names, or all of them, if no iterable is provided.

Complies with SVG v1.1
Authoring best practices: https://jwatt.org/svg/authoring/

Only a dozen or so element types are explicitly supported, but arbitary XML may be inlined via the Element class.

API Documentation is lacking, but the samples should help.
