import socket


class PortKnocker(object):
    class HostError(Exception):
        pass

    def __init__(self, remote, host):
        self._remote = remote

        if host is None:
            self._address = None
        else:
            try:
                addresses = socket.getaddrinfo(
                        host, 42,
                        socket.AF_UNSPEC, socket.SOCK_STREAM)
            except socket.gaierror:
                addresses = None
            if not addresses:
                raise PortKnocker.HostError(
                        _(u"Could lookup {hostname}").format(
                                hostname=host))
            if len(addresses) > 1:
                print _(u"Hostname {hostname} resolved to multiple addresses:")
                for i, (af, socktype, proto, canonname, sa) in addresses:
                    print u"  %s%s" % (
                            canonname, i == 0 and
                            u" " + _(u"(selected)")
                            or u"")
            self._address = addresses[0]

    def run(self, client, ports):
        if client:
            self._connect()
            self._listen(ports)
        else:
            self._listen(ports)
            self._connect()

    def _listen(self, ports):
        results = []
        for port in ports:
            # TODO : listen on port
            self._remote.send_msg('testport %d' % port)
            rep = self._remote.recv_msg()
            results.append((port, rep))
            # TODO : close port
        return results

    def _connect(self):
        results = []
        req = self._remote.recv_msg()
        if req.startswith('testport '):
            port = int(req[9:])
            r = self._try_connect(port)
            results.append((port, r))
            self._remote.send_msg(r)
        return results

    def _try_connect(self, port):
        af, socktype, proto, canonname, sa = self._address
        # TODO : change port from 42 to port
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error:
            return 'error'
        s.settimeout(5)
        try:
            s.connect(sa)
        except socket.error:
            return 'closed'
        else:
            return 'open'
        finally:
            s.close()

    def _show(self, results):
        total = dict(open=0, closed=0)
        def describe(result):
            if result == 'open':
                total['open'] += 1
                return _(u"open")
            elif result == 'closed':
                total['closed'] += 1
                return _(u"closed")
        print _(u"Port        Status")
        for port, result in results:
            p = "%d" % port
            p += " " * (12 - len(p))
            print "%s%s" % (p, describe(result))
        print "--------------------"
        print _(u"Total: {open} open, {closed} closed").format(
                open=total['open'], closed=total['closed'])
