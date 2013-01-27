import Queue as queue
from threading import Thread


class Remote(object):
    def __init__(self, istream, ostream, delim='\n'):
        self._istream = istream
        self._ostream = ostream

        if not isinstance(delim, str):
            raise TypeError("Process: expected argument delim to be of type "
                            "str, got %r" % type(delim))
        if len(delim) != 1:
            raise ValueError("Process: expected argument delim to be a "
                             "single-character string, got %r" % delim)
        self._delim = delim

        self._sendq = queue.Queue()
        self._recvq = queue.Queue()

        r = Thread(target=self._reading_thread)
        r.setDaemon(True)
        r.start()

        w = Thread(target=self._writing_thread)
        w.setDaemon(True)
        w.start()

    def send_msg(self, msg):
        self._sendq.put(msg)

    def recv_msg(self):
        return self._recvq.get()

    def _reading_thread(self):
        buf = ''
        while True:
            data = self._istream.read(64)
            p = data.find(self._delim)
            while p != -1:
                msg, buf, data = buf + data[:p], '', data[p+1:]
                self._recvq.put(msg)
                p = data.find(self._delim)
            buf += data

    def _writing_thread(self):
        while True:
            self._ostream.write(self._sendq.get())
