
SimpleSVG creates Inkscape-aware SVG documents with support for layers and groups.

Documentation is lacking, but the samples should help.

makesvg1.py creates an intricate document with complementary layers, grouping, and simple command-line argument parsing. By adjusting the visibility of the layers, various flavors of the result are obtained that are more appropriate for export to bitmap at a given resolution. Inkscape can be used in a command-line/batch mode to create these bitmaps.

makesvg2a.py and makesvg2b.py create the same very simple single-path document that is intended for uploading to Ponoko.

I think the most notable items are that all motions are relative, and that there are no external dependencies, not even any from the Standard Libary. Functionality is limited, but extension is straightforward, as additional elements and attributes may be arbitrarily included.
