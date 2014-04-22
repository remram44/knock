import select
import socket
import sys


class Listener(object):
    class Error(Exception):
        pass

    def __init__(self, port):
        self._sockets = []

        self._try_listen(socket.AF_INET, port)
        if socket.has_ipv6:
            self._try_listen(socket.AF_INET6, port)

        if not self._sockets:
            raise Listener.Error

    def _try_listen(self, af, port):
        try:
            s = socket.socket(af, socket.SOCK_STREAM)
            s.bind(('', port))
            s.listen(5)
            self._sockets.append(s)
        except socket.error:
            pass

    def accept(self):
        for s in self._sockets:
            ready_read, ready_write, errors = select.select(
                    [s], [], [], 0)
            if ready_read:
                c = s.accept()
                if c is not None:
                    c[0].close()

    def close(self):
        for s in self._sockets:
            s.close()


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
                        _(u"Couldn't lookup {hostname}").format(
                                hostname=host))
            if len(addresses) > 1:
                print >>sys.stderr, _(u"Hostname {hostname} resolved to "
                                      "multiple addresses:").format(
                                              hostname=host)
                for i, info in enumerate(addresses):
                    af, socktype, proto, canonname, sa = info
                    if i == 0:
                        sel = u" " + _(u"(selected)")
                    else:
                        sel = u""
                    print >>sys.stderr, u"  %s%s" % (sa[0], sel)
            self._address = addresses[0]

    def run(self, client, ports):
        if client:
            r_results = self._connect()
            l_results = self._listen(ports)
            if r_results:
                print _(u"\nResults for ports scanned on the remote machine:")
                self._show(r_results)
            if l_results:
                print _(u"\nResults for ports scanned on the local machine:")
                self._show(l_results)
        else:
            self._listen(ports)
            self._connect()

    def _listen(self, ports):
        results = []
        for port in ports:
            try:
                listen = Listener(port)
                self._remote.send_msg('testport %d' % port)
                listen.accept()
                rep = self._remote.recv_msg()
                results.append((port, rep))
                listen.close()
            except Listener.Error:
                self._remote.send_msg('skippedport %d' % port)
                results.append((port, 'error'))
        self._remote.send_msg('endtests')
        return results

    def _connect(self):
        results = []
        while True:
            req = self._remote.recv_msg()
            if req.startswith('testport '):
                port = int(req[9:])
                r = self._try_connect(port)
                results.append((port, r))
                self._remote.send_msg(r)
            elif req.startswith('skippedport '):
                port = int(req[12:])
                results.append((port, 'skipped'))
            elif req == 'endtests':
                break
        return results

    def _try_connect(self, port):
        af, socktype, proto, canonname, sa = self._address

        # Set port
        sa = (sa[0], port)

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

    @staticmethod
    def _show(results):
        total = dict(open=0, closed=0, error=0)
        def describe(result):
            if result == 'open':
                total['open'] += 1
                return _(u"open")
            elif result == 'closed':
                total['closed'] += 1
                return _(u"closed")
            elif result == 'skipped':
                total['error'] += 1
                return _(u"remote skipped")
            elif result == 'error':
                total['error'] += 1
                return _(u"local error")
            else:
                return repr(result)
        print _(u"Port        Status")
        for port, result in results:
            p = "%d" % port
            p += " " * (12 - len(p))
            print "%s%s" % (p, describe(result))
        print "--------------------"
        print _(u"Total: {open} open, {closed} closed").format(
                open=total['open'], closed=total['closed'])
