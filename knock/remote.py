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
        self._closed = False

        self._recvq = queue.Queue()
        self._sendq = queue.Queue()

        self._r_thread = Thread(target=self._reading_thread)
        self._r_thread.setDaemon(True) # I don't know how to stop this one
        self._r_thread.start()

        self._w_thread = Thread(target=self._writing_thread)
        self._w_thread.start()

    def recv_msg(self):
        return self._recvq.get()

    def send_msg(self, msg):
        self._sendq.put(msg)

    def _reading_thread(self):
        buf = ''
        while True:
            data = self._istream.read(1)
            if self._closed or not data:
                break
            if data == self._delim:
                msg, buf = buf, ''
                self._recvq.put(msg)
            else:
                buf += data

    def _writing_thread(self):
        while True:
            msg = self._sendq.get()
            if msg is None:
                break
            self._ostream.write(msg + self._delim)
            self._ostream.flush()

    def close(self):
        self._closed = True
        # No idea how to stop this one...

        self._sendq.put(None)
        self._w_thread.join()
