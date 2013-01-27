from bisect import bisect
import itertools
import re


__all__ = ['PortList']


_port_spec = re.compile(r'^([0-9]+)(?:-([0-9]+))?$')


class PortList(object):
    def __init__(self):
        self._ranges = [] # [(port: int, port: int), ...]

    def add_range(self, first, last=None):
        if last is None:
            last = first

        # Find insertion pos
        pos = bisect(self._ranges, (first, last))

        # We might overlap with the range immediately left, plus any number of
        # ranges right
        if pos > 0 and first <= self._ranges[pos-1][1] + 1:
            self._ranges[pos-1] = self._ranges[pos-1][0], last
            pos -= 1
        else:
            self._ranges.insert(pos, (first, last))

        # Merge right
        while (pos+1 < len(self._ranges) and
                self._ranges[pos+1][0]+1 <= self._ranges[pos][1]):
            self._ranges[pos] = (
                self._ranges[pos][0],
                max(self._ranges[pos][1], self._ranges[pos+1][1]))
            del self._ranges[pos+1]

    def add(self, spec):
        # Try to match a port spec
        m = _port_spec.match(spec)
        if m is None:
            return False
        else:
            first, last = m.groups()
            if last is None:
                last = first
            elif last < first:
                raise ValueError(_(u"Port sequence goes backwards: "
                                   "{0}-{1}").format(first, last))
            try:
                first, last = int(first), int(last)
            except ValueError:
                raise ValueError(_(u"Port spec couldn't be parsed"))
            self.add_range(first, last)
            return True

    def to_arglist(self):
        l = []
        for first, last in self._ranges:
            if first == last:
                l.append(str(first))
            else:
                l.append(b"%d-%d" % (first, last))
        return l

    def __str__(self):
        return ",".join(self.to_arglist())

    def _iter_ranges(self):
        for first, last in self._ranges:
            yield xrange(first, last+1)

    def __iter__(self):
        return itertools.chain.from_iterable(self._iter_ranges())
