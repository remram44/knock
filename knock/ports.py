import re


__all__ = ['PortList']


_port_spec = re.compile(r'^([0-9]+)(?:-([0-9]+))?$')


class PortList(object):
    def __init__(self):
        self._ranges = [] # [(port: int, port: int), ...]

    def add_range(self, first, last=None):
        pass # TODO : can be scavenged from Yoppi

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
        return self.to_arglist().join(",")
