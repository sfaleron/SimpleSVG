
``rounded_notch_old.py`` and ``rounded_notch_new.py`` create the same very simple single-path document that is intended for uploading to Ponoko, using an old API for making ninety degree turns, and a newer `Turtle`_-inspired drawing class, respectively.

``turntests.py`` has two parts:

- Demonstration of ``NotTurtle``: a repeating pattern, with a quarter-turn each time.
- Demonstration of ``RoundedRect``: a collection of disjoint figures demonstrating the  class, which inherits from ``NotTurtle`` and allows for individual control of each corner's radius.

You might also check out my `TriPhi`_ repository, which spun off from this one
when it grew sufficiently sophisticated. I wrote this library to support creating
the SVGs it produces. In particular, ``svg/unitpair.svg`` is an (ahem) "real-life"
example using the decorations from the add-on simplesvgmath package.

.. _Ponoko: https://www.ponoko.com/starter-kits/inkscape
.. _Turtle: https://en.wikipedia.org/wiki/Turtle_graphics
.. _TriPhi: https://github.com/sfaleron/TriPhi
