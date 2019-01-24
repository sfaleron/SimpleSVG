
from __future__ import absolute_import

from    .styled import StyledElement


# only relative movements!
class Path(StyledElement):
    def __init__(self, initial_pos, **attrs):
        StyledElement.__init__(self, 'path', **attrs)
        self.steps = ['M%s,%s' % tuple(initial_pos)]

    def moveTo(self, pt):
        self.steps.append('m%s %s' % tuple(pt))

    def lineTo(self, pt):
        self.steps.append('l%s %s' % tuple(pt))

    def lineToMany(self, many):
        self.steps.append('l' + 'l'.join(['%s %s' % tuple(i) for i in many]))

    def arcTo(self, pt, rx, ry, rot, bigArc=False, incAngle=True):
        """https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes"""
        self.steps.append('a%s,%s %s %s,%s %s,%s' %
            (rx, ry, rot, int(bool(bigArc)), int(bool(incAngle)), pt[0], pt[1]))

    def close(self):
        return self.steps.append('z')

    def __str__(self):
        self['d'] = '\n'.join(self.steps)
        return StyledElement.__str__(self)

