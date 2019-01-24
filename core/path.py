
from __future__ import absolute_import

from    .styled import StyledElement


class PathOps(object):
    def __init__(self, host, absolute):
        self._host     = host
        self._absolute = absolute

    def _fmt(self, opIn, fmtIn=None):
        opOut = opIn.upper() if self._absolute else opIn

        return opOut if fmtIn is None else '{} {}'.format(opOut, fmtIn)

    def _op(self, cmd, formatOnly):
        if formatOnly:
            return cmd
        else:
            self._host.append(cmd)

    def moveTo(self, pt, formatOnly=False):
        return self._op(self._fmt('m', '{} {}').format(*pt), formatOnly)

    def lineTo(self, pt, formatOnly=False):
        return self._op(self._fmt('l', '{} {}').format(*pt), formatOnly)

    def lineToH(self, x, formatOnly=False):
        return self._op(self._fmt('h', '{}').format(x), formatOnly)

    def lineToV(self, y, formatOnly=False):
        return self._op(self._fmt('v', '{}').format(y), formatOnly)

    def arcTo(self, pt, rx, ry, rot, bigArc=False, incAngle=True, formatOnly=False):
        """https://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes"""

        return self._op(self._fmt('a', '{},{} {} {},{} {},{}').format(rx, ry, rot,
            int(bool(bigArc)), int(bool(incAngle)), *pt), formatOnly)

    def lineToMany(self, many, formatOnly=False):
        return self._op(' '.join([self._fmt('l', '{} {}').format(*pt) for pt in many]), formatOnly)

    def close(self, formatOnly=False):
        return self._op(self._fmt('z'), formatOnly)


class Path(StyledElement):
    def __init__(self, initial_pos, **attrs):
        StyledElement.__init__(self, 'path', **attrs)

        self.rel = PathOps(self, False)
        self.abs = PathOps(self, True)

        self._steps = []

        self.abs.moveTo(initial_pos)

    def append(self, e):
        self._steps.append(e)

    def lineToMany(self, start, many, formatOnly=False):
        """Absolute-relative combination"""

        cmd = '{} {}'.format(
            self.abs.moveTo(   start, formatOnly=True),
            self.rel.lineToMany(many, formatOnly=True) )

        if formatOnly:
            return cmd
        else:
            self.append(cmd)

    def close(self, formatOnly=False):
        return self.rel.close(formatOnly)


    @property
    def steps(self):
        return self._steps

    def __str__(self):
        self['d'] = '\n'.join(self._steps)
        return StyledElement.__str__(self)
