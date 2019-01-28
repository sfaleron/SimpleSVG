
from __future__ import absolute_import

from    .base   import Element, register


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
            int(bigArc), int(incAngle), *pt), formatOnly)

    def lineToMany(self, many, formatOnly=False):
        return self._op(' '.join([self._fmt('l', '{} {}').format(*pt) for pt in many]), formatOnly)

    def close(self, formatOnly=False):
        return self._op(self._fmt('z'), formatOnly)


@register('path', 'styled')
class Path(Element):
    def __init__(self, initial_pos=None, **attrs):
        """May provide initial position or any valid value for the 'd'
        attribute. If the initial position is provided, any initial
        value will be overwritten."""

        Element.__init__(self, **attrs)

        self.rel = PathOps(self, False)
        self.abs = PathOps(self, True)

        self._all_init()
        self._steps = []

        if initial_pos is None:
            if not attrs.get('d', '')[0].lower() == 'm':
                raise ValueError("Must provide an initial position or a valid 'd' attribute.")
            else:
                self._steps.append(attrs[d])
        else:
            self.abs.moveTo(initial_pos)

    def _all_init(self):
        self.rel = PathOps(self, False)
        self.abs = PathOps(self, True)

    def _copy_init(self, src):
        self._all_init()
        self._steps = src.steps[:]
        Element._copy_init(self, src)

    def _import_init(self):
        self._all_init()
        self._steps = [self.pop('d')] if 'd' in self else []
        Element._import_init(self, src)

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
        return Element.__str__(self)
