import gzip
import os
import subprocess


class KaldiPipe(object):
    def __init__(self, process, rxtype):
        self.out_stream = process.stdout
        self.rxtype = rxtype

    def close(self):
        self.wait()

    def bytes(self):
        if not hasattr(self, "__bytes"):
            self.__bytes = self.out_stream.read()
        return self.__bytes


class KaldiFile(object):
    def __init__(self, filename, rxtype=None, is_gz=False):
        self.filename = filename
        self.is_gz = is_gz
        if rxtype is None:
            rxtype = _get_specifier_type(filename)
        self.rxtype = rxtype

    def __getstate__(self):
        # Add file stats to pickle for timestamp uniqueness
        state = dict(self.__dict__)
        state['__filestate'] = (os.path.getctime(self.filename), os.path.getmtime(self.filename))
        return state


class KaldiGzFile(KaldiFile):
    def __init__(self, filename, rxtype):
        super().__init__(filename, rxtype=rxtype, is_gz=True)


class KaldiBytes(object):
    def __init__(self, bytes, rxtype):
        self.bytes = bytes
        self._rxtype = rxtype


def _get_specifier_type(filename):
    if filename.endswith('.scp'):
        return 'scp'
    elif filename.endswith('.ark'):
        return 'ark'
    else:
        return 'ark'
