import gzip
import os
import subprocess


class KaldiPipe(object):
    def __init__(self, process, *_, rxtype):
        self.wait = process.wait
        self.out_stream = process.stdout
        self.rxtype = rxtype

    def close(self):
        self.wait()

    @property
    def bytes(self):
        if not hasattr(self, "_bytes"):
            self._bytes = self.out_stream.read()
        return self._bytes


class KaldiFile(object):
    def __init__(self, filename, *_, rxtype, is_gz=False):
        self.filename = filename
        self.is_gz = is_gz
        self.rxtype = rxtype

    def __getstate__(self):
        # Add file stats to pickle for timestamp uniqueness
        state = dict(self.__dict__)
        state['__filestate'] = (os.path.getctime(self.filename), os.path.getmtime(self.filename))
        return state


class KaldiGzFile(KaldiFile):
    def __init__(self, filename, *_, rxtype):
        super().__init__(filename, rxtype=rxtype, is_gz=True)


class KaldiBytes(object):
    def __init__(self, bytes, *_, rxtype):
        self.bytes = bytes
        self.rxtype = rxtype


class KaldiBytesArk(KaldiBytes):
    def __init__(self, dict):
        super().__init__(dict, rxtype='ark')

    @property
    def bytes(self):
        return b''.join([
            id.encode() + b' ' + b for id, b in self._bytes.items()
        ])

    @bytes.setter
    def bytes(self, value):
        self._bytes = value
